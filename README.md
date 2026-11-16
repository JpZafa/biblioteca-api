# API de Consulta ao Acervo de uma Biblioteca

Atividade acadêmica desenvolvida em Python com FastAPI. Permite listar o acervo e consultar um livro pelo identificador. Os cinco livros iniciais ficam em memória, no repositório; não é necessário instalar banco de dados.

## Requisitos

- Python 3.10 ou superior, com pip.
- Terminal aberto na pasta `biblioteca-api`, onde está o arquivo `main.py`.

As versões das dependências estão fixadas nos arquivos `requirements*.txt` para reproduzir o ambiente usado na validação.

## Executar no Windows (PowerShell)

Extraia o ZIP, abra a pasta `biblioteca-api` no VS Code e abra um terminal nessa pasta. Execute, um comando por vez:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Se o comando `py` não existir, use `python -m venv .venv` na primeira linha. Não é necessário ativar o ambiente virtual usando esses comandos.

## Executar no Linux/macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

## Acessar e testar

Com o servidor iniciado, abra:

- Documentação interativa: <http://127.0.0.1:8000/docs>
- Listagem dos livros: <http://127.0.0.1:8000/livros>
- Livro de identificador 1: <http://127.0.0.1:8000/livros/1>

Na documentação, expanda uma rota, clique em **Try it out**, preencha o identificador quando necessário e clique em **Execute**. A rota `/` não foi criada; use os endereços acima. Para encerrar o servidor, pressione `Ctrl+C` no terminal.

| Método | Endereço | Resultado esperado |
|---|---|---|
| GET | `/livros` | 200 e uma lista JSON com cinco livros |
| GET | `/livros/1` | 200 e o livro correspondente |
| GET | `/livros/999` | 404 e uma mensagem de livro não encontrado |
| GET | `/livros/0` | 422: identificador deve ser maior que zero |
| GET | `/livros/-1` | 422: identificador deve ser maior que zero |
| GET | `/livros/abc` | 422: identificador deve ser inteiro |
| GET | `/livros/1.5` | 422: identificador deve ser inteiro |

Exemplo de resposta de `GET /livros/1`:

```json
{
  "id": 1,
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano_publicacao": 1899,
  "disponivel": true
}
```

Exemplo de resposta de `GET /livros/999`:

```json
{
  "detail": "Livro com id 999 não encontrado."
}
```

## Organização e decisões

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Definir as rotas, validar a URL, declarar respostas e converter a exceção de domínio em HTTP 404 |
| `models.py` | Definir o modelo `Livro`, suas validações e o modelo da resposta 404 |
| `repository.py` | Manter o acervo em memória e realizar as consultas |
| `exceptions.py` | Declarar a exceção `LivroNaoEncontrado`, sem depender de HTTP |
| `tests/test_api.py` | Verificar as rotas, as validações e o comportamento do repositório |
| `requirements.txt` | Dependências necessárias para executar a API |
| `requirements-dev.txt` | Dependências adicionais para executar os testes |

- `id` e `ano_publicacao` são inteiros estritamente positivos; booleanos, textos e números fracionários não são aceitos nesses campos do modelo.
- `titulo` e `autor` são obrigatórios. Espaços externos são removidos antes da validação; textos vazios ou compostos somente por espaços são rejeitados.
- `disponivel` deve ser booleano. Todos os campos são obrigatórios.
- O identificador da URL usa `int` com `Path(gt=0)`. O FastAPI responde automaticamente com 422 para valores inválidos.
- As rotas de sucesso declaram `response_model`; a resposta 404 também tem modelo documentado.
- O repositório lança `LivroNaoEncontrado` quando não há correspondência. A API captura essa exceção e gera HTTP 404.
- A API acessa o acervo somente pelos métodos do repositório. A dependência `obter_repositorio` permite substituir o acervo nos testes.
- `LivroRepository([])` representa um acervo vazio: a listagem retorna 200 com `[]`, e a busca por um identificador positivo retorna 404. Esse cenário é verificado nos testes sem modificar o acervo inicial.
- Os objetos `Livro` são imutáveis, e a listagem devolve uma cópia da coleção.
- Não existem operações de cadastro, edição ou exclusão, pois a atividade exige apenas consultas.

## Testes automatizados

Os testes usam `unittest`, da biblioteca padrão, e `TestClient`, do FastAPI. No Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

No Linux/macOS:

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
```

São dez testes, com casos adicionais para cada identificador e dado inválido. Cobrem a listagem, os cinco livros, livro inexistente, identificadores inválidos, acervo vazio, campos obrigatórios, tipos e limites dos campos, remoção de espaços, exceção de domínio, proteção da coleção e documentação OpenAPI.

## Publicar e entregar no GitHub

1. Acesse <https://github.com/new> e crie um repositório chamado `biblioteca-api`. Para facilitar o acesso do professor, use a visibilidade pública se a instituição não orientar de outra forma.
2. Na página do repositório, use **uploading an existing file** ou **Add file > Upload files**.
3. Envie os arquivos de dentro da pasta `biblioteca-api`, incluindo a pasta `tests`. Envie também `.gitignore`; não envie `.venv`, `__pycache__` nem o ZIP.
4. Confirme o envio em **Commit changes**.
5. Verifique se o `README.md` e o `main.py` aparecem na raiz do repositório.
6. Copie o endereço do repositório exibido no navegador e entregue esse link na atividade.

## Referências

- [FastAPI: modelos de resposta](https://fastapi.tiangolo.com/tutorial/response-model/)
- [FastAPI: parâmetros e validação numérica](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
- [FastAPI: tratamento de erros](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Pydantic: tipos e restrições](https://docs.pydantic.dev/latest/api/types/)
