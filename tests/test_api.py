"""Testes dos comportamentos exigidos no enunciado."""

import unittest

from fastapi.testclient import TestClient
from pydantic import ValidationError

from exceptions import LivroNaoEncontrado
from main import app, obter_repositorio
from models import Livro
from repository import LivroRepository


class BibliotecaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repositorio = LivroRepository()
        app.dependency_overrides[obter_repositorio] = lambda: self.repositorio
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.clear()

    def test_listagem_retorna_cinco_livros_validos(self) -> None:
        resposta = self.client.get("/livros")
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.json()
        self.assertIsInstance(dados, list)
        self.assertEqual(len(dados), 5)
        self.assertEqual(len({item["id"] for item in dados}), 5)
        for item in dados:
            self.assertEqual(Livro.model_validate(item).model_dump(), item)

    def test_consulta_cada_livro(self) -> None:
        for livro in self.repositorio.listar():
            with self.subTest(livro_id=livro.id):
                resposta = self.client.get(f"/livros/{livro.id}")
                self.assertEqual(resposta.status_code, 200)
                self.assertEqual(resposta.json(), livro.model_dump())

    def test_livro_inexistente_retorna_404(self) -> None:
        resposta = self.client.get("/livros/999")
        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.json(), {"detail": "Livro com id 999 não encontrado."})

    def test_identificadores_invalidos_retornam_422(self) -> None:
        for identificador in ("0", "-1", "abc", "1.5"):
            with self.subTest(identificador=identificador):
                resposta = self.client.get(f"/livros/{identificador}")
                self.assertEqual(resposta.status_code, 422)
                self.assertEqual(resposta.json()["detail"][0]["loc"], ["path", "livro_id"])

    def test_acervo_vazio(self) -> None:
        self.repositorio = LivroRepository([])
        resposta = self.client.get("/livros")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json(), [])
        self.assertEqual(self.client.get("/livros/1").status_code, 404)

    def test_modelo_rejeita_dados_invalidos(self) -> None:
        valido = self.repositorio.buscar_por_id(1).model_dump()
        casos = {
            "id": [0, -1, "1", True, 1.5],
            "titulo": ["", "   ", None, 12],
            "autor": ["", "   ", None, 12],
            "ano_publicacao": [0, -1, "2000", True, 2000.5],
            "disponivel": ["true", 1, None],
        }
        for campo, valores in casos.items():
            for valor in valores:
                with self.subTest(campo=campo, valor=valor):
                    with self.assertRaises(ValidationError):
                        Livro.model_validate({**valido, campo: valor})
        for campo in valido:
            with self.subTest(campo_ausente=campo):
                with self.assertRaises(ValidationError):
                    Livro.model_validate({k: v for k, v in valido.items() if k != campo})

    def test_modelo_remove_espacos_externos(self) -> None:
        dados = self.repositorio.buscar_por_id(1).model_dump()
        livro = Livro.model_validate({**dados, "titulo": "  Livro  ", "autor": " Autor "})
        self.assertEqual(livro.titulo, "Livro")
        self.assertEqual(livro.autor, "Autor")

    def test_repositorio_lanca_excecao_de_dominio(self) -> None:
        with self.assertRaises(LivroNaoEncontrado):
            self.repositorio.buscar_por_id(999)

    def test_listagem_nao_expoe_colecao_interna(self) -> None:
        lista = self.repositorio.listar()
        lista.clear()
        self.assertEqual(len(self.repositorio.listar()), 5)

    def test_openapi_documenta_respostas_e_validacao(self) -> None:
        schema = self.client.get("/openapi.json").json()
        listagem = schema["paths"]["/livros"]["get"]
        consulta = schema["paths"]["/livros/{livro_id}"]["get"]
        self.assertEqual(listagem["responses"]["200"]["content"]["application/json"]["schema"]["type"], "array")
        self.assertTrue({"200", "404", "422"}.issubset(consulta["responses"]))
        self.assertEqual(consulta["parameters"][0]["schema"]["exclusiveMinimum"], 0)


if __name__ == "__main__":
    unittest.main()
