"""Exceções de domínio, independentes do protocolo HTTP."""


class LivroNaoEncontrado(Exception):
    def __init__(self, livro_id: int) -> None:
        super().__init__(f"Livro com id {livro_id} não encontrado.")
