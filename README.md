# BMVC - Portal e Banco de Filmes

## Texto explicativo

O sistema foi desenvolvido a partir do framework BMVC (Bottle + MVC), mantendo a mesma arquitetura do projeto base. As rotas ficam em `route.py`. O controlador `Application` administra as páginas pelo dicionário `pages` e é composto por um objeto `DataRecord`, que persiste os modelos em arquivos JSON na pasta `app/controllers/db`. Os modelos `UserAccount` e `Filme` ficam em `app/models`, e as páginas `.tpl` em `app/views/html`.

O recurso **portal** (`/portal`) faz o login dos usuários com o modelo `UserAccount`. Quando o login dá certo, o `DataRecord` gera um `session_id` com `uuid`, e esse valor é gravado em um cookie que passa a identificar o usuário. O recurso **banco** (`/banco`) só pode ser acessado por usuários autenticados e apresenta a lista de filmes cadastrados. O tema escolhido foi `Filme`, com os atributos titulo, diretor e ano.

O READ é feito no próprio sistema, na página `/banco`. O CREATE (`POST /banco`), o UPDATE (`PUT /banco/<id>`) e o DELETE (`DELETE /banco/<id>`) são feitos obrigatoriamente via cURL, no terminal Linux. Para isso, o cURL envia o cookie de sessão recebido no login do portal. Os comandos estão mais abaixo.

## Recursos

- **portal** (`/portal`): login de usuários, modelo `UserAccount`.
- **banco** (`/banco`): só pode ser acessado por usuários autenticados e mostra a lista de filmes cadastrados, modelo `Filme` (atributos: titulo, diretor e ano).

## Arquitetura

- `route.py`: rotas do sistema.
- `app/controllers/application.py`: controlador `Application`, que administra as páginas pelo dicionário `pages` e tem um objeto `DataRecord` (composição).
- `app/controllers/datarecord.py`: classe `DataRecord`, que lê e grava os modelos nos arquivos JSON da pasta `app/controllers/db` e controla as sessões dos usuários (`session_id` gerado com `uuid`).
- `app/models/`: modelos `UserAccount` e `Filme`.
- `app/views/html/`: páginas `portal.tpl` e `banco.tpl`.

## CRUD

| Operação | Método e rota | Onde é feita |
| --- | --- | --- |
| READ | `GET /banco` | no próprio sistema (navegador) |
| CREATE | `POST /banco` | cURL |
| UPDATE | `PUT /banco/<id>` | cURL |
| DELETE | `DELETE /banco/<id>` | cURL |

As rotas de CREATE, UPDATE e DELETE também exigem login: o cURL precisa enviar o cookie `session_id` recebido no portal.

## Como executar

```bash
pip install bottle
python3 route.py
```

Acesse http://localhost:8080/portal e entre com `Henrique` / `123456` (ou `Moura` / `456789`).

## Comandos cURL (terminal Linux)

```bash
# 1. Login no portal (salva o cookie da sessão em cookies.txt)
curl -c cookies.txt -d "username=Henrique&password=123456" http://localhost:8080/portal

# 2. CREATE - cadastra um filme
curl -b cookies.txt -X POST -d "titulo=Tropa de Elite&diretor=José Padilha&ano=2007" http://localhost:8080/banco

# 3. UPDATE - altera o filme de id 3
curl -b cookies.txt -X PUT -d "ano=2008" http://localhost:8080/banco/3

# 4. DELETE - remove o filme de id 3
curl -b cookies.txt -X DELETE http://localhost:8080/banco/3
```

Depois de cada comando, basta atualizar a página `/banco` no navegador para ver a lista atualizada (READ).
