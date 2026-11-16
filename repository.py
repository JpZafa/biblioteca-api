"""Armazenamento em memória e consultas ao acervo."""

from exceptions import LivroNaoEncontrado
from models import Livro


class LivroRepository:
    def __init__(self, livros: list[Livro] | None = None) -> None:
        # None carrega o acervo inicial; [] representa um acervo vazio.
        self._livros = list(livros) if livros is not None else [
            Livro(id=1, titulo="Dom Casmurro", autor="Machado de Assis",
                  ano_publicacao=1899, disponivel=True),
            Livro(id=2, titulo="O Cortiço", autor="Aluísio Azevedo",
                  ano_publicacao=1890, disponivel=False),
            Livro(id=3, titulo="Vidas Secas", autor="Graciliano Ramos",
                  ano_publicacao=1938, disponivel=True),
            Livro(id=4, titulo="A Hora da Estrela", autor="Clarice Lispector",
                  ano_publicacao=1977, disponivel=True),
            Livro(id=5, titulo="Capitães da Areia", autor="Jorge Amado",
                  ano_publicacao=1937, disponivel=False),
        ]

    def listar(self) -> list[Livro]:
        # Retorna uma cópia para proteger a coleção interna.
        return list(self._livros)

    def buscar_por_id(self, livro_id: int) -> Livro:
        for livro in self._livros:
            if livro.id == livro_id:
                return livro
        raise LivroNaoEncontrado(livro_id)
