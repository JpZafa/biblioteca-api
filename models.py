"""Modelos e regras de validação dos dados da biblioteca."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


TextoObrigatorio = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, strict=True)
]


class Livro(BaseModel):
    # Impede alterações que possam invalidar um livro já cadastrado.
    model_config = ConfigDict(frozen=True)

    id: Annotated[int, Field(gt=0, strict=True)]
    titulo: TextoObrigatorio
    autor: TextoObrigatorio
    ano_publicacao: Annotated[int, Field(gt=0, strict=True)]
    disponivel: Annotated[bool, Field(strict=True)]


class ErroResposta(BaseModel):
    detail: str
