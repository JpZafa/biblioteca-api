"""Camada HTTP: rotas, respostas e tradução de erros de domínio."""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, status

from exceptions import LivroNaoEncontrado
from models import ErroResposta, Livro
from repository import LivroRepository


app = FastAPI(
    title="API da Biblioteca",
    description="Consulta ao acervo de livros armazenado em memória.",
    version="1.0.0",
)

_repositorio = LivroRepository()


def obter_repositorio() -> LivroRepository:
    """Fornece a mesma instância durante a execução da aplicação."""
    return _repositorio


@app.get("/livros", response_model=list[Livro], tags=["Livros"],
         summary="Listar todos os livros")
def listar_livros(
    repositorio: Annotated[LivroRepository, Depends(obter_repositorio)],
) -> list[Livro]:
    return repositorio.listar()


@app.get(
    "/livros/{livro_id}",
    response_model=Livro,
    responses={404: {"model": ErroResposta, "description": "Livro não encontrado"}},
    tags=["Livros"],
    summary="Consultar um livro pelo identificador",
)
def consultar_livro(
    livro_id: Annotated[int, Path(gt=0, description="Identificador inteiro positivo")],
    repositorio: Annotated[LivroRepository, Depends(obter_repositorio)],
) -> Livro:
    # FastAPI valida a URL e responde 422 antes de executar esta função.
    try:
        return repositorio.buscar_por_id(livro_id)
    except LivroNaoEncontrado as erro:
        # O repositório conhece o domínio; somente a API conhece HTTP.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
