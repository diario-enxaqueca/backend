# Diário de Enxaqueca – Backend

Backend do projeto **Diário de Enxaqueca**, desenvolvido na disciplina Técnicas de Programação em Plataformas Emergentes / Engenharia de Software – UNB Gama.
Este repositório contém a implementação do **MVP** utilizando **Python**, **FastAPI**, **SQLAlchemy**, **MySQL**, seguindo boas práticas de **Clean Code**, **SOLID** e **UX**.

## Índice

* Visão Geral
* MVP
* Backlog
* Tecnologias
* Estrutura do Projeto
* Instalação e Configuração
* Executando com Docker
* API
* Testes
* Contribuição
* Licença

## Visão Geral

O projeto tem como objetivo fornecer **uma aplicação CRUD** para registro e acompanhamento de enxaquecas, permitindo ao usuário:
* Criar registros de enxaqueca com informações como intensidade, gatilhos, medicação e observações.
* Consultar, atualizar e excluir registros existentes.
* Testar a funcionalidade de forma estruturada utilizando testes automatizados.

A aplicação segue o **padrão MVC**, com código organizado em `source/` e subpastas para cada regra de negócio.

## MVP

Para a primeira entrega, o MVP contempla:

Cadastro e gerenciamento de **registros de enxaqueca** (CRUD completo).

Backend funcional com **FastAPI**, **MySQL** via **SQLAlchemy** e documentação **Swagger** automática.

Estrutura de testes básica, com pelo **um teste skipado** para demonstrar configuração de testes.

Preparação para integração futura com frontend em **React.js + TypeScript**.

## Backlog

Lista de 10 histórias de usuário simplificadas para o MVP:

| #  | História de Usuário                                          | Regras de Negócio                                           |
| -- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| 1  | Como usuário, quero me cadastrar para acessar meus registros | Cadastro único por e-mail                                   |
| 2  | Como usuário, quero fazer login para acessar meus registros  | Autenticação via JWT                                        |
| 3  | Como usuário, quero criar registros de enxaqueca             | Campos: data, intensidade, gatilhos, medicação, observações |
| 4  | Como usuário, quero listar meus registros                    | Listar apenas registros do usuário logado                   |
| 5  | Como usuário, quero atualizar registros                      | Permitir edição de qualquer campo                           |
| 6  | Como usuário, quero excluir registros                        | Exclusão física do registro                                 |
| 7  | Como desenvolvedor, quero documentação da API                | Usar Swagger / FastAPI docs                                 |
| 8  | Como desenvolvedor, quero testes unitários                   | Testes com pytest para endpoints CRUD                       |
| 9  | Como usuário, quero protótipo visual                         | Interface seguindo protótipo Figma MVP                      |
| 10 | Como desenvolvedor, quero deploy com Docker                  | Backend e MySQL dockerizados                                |

## Tecnologias

* Linguagem: Python 3.10+
* Framework: FastAPI
* Banco de Dados: MySQL (dockerizado)
* ORM: SQLAlchemy
* Documentação da API: Swagger
* Testes: Pytest
* Docker & Docker Compose
* Padrões de código: Clean Code, SOLID, Lint

## Estrutura do Projeto
```code
diario-enxaqueca-backend/
│
├── source/
│   ├── main.py           # Chama as rotas
│   ├── config.py         # Configurações do projeto
│   ├── registros/        # Regra de negócio: CRUD de registros
│   │   ├── model_registro.py
│   │   ├── view_registro.py
│   │   ├── controller_registro.py
│   │   └── teste_registro.py
│   └── usuario/          # Futuro CRUD de usuários
│       ├── model_usuario.py
│       ├── view_usuario.py
│       ├── controller_usuario.py
│       └── teste_usuario.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Instalação e Configuração

Clone o repositório:
```code
git clone https://github.com/sua-org/diario-enxaqueca-backend.git
cd diario-enxaqueca-backend
```

Crie um arquivo .env na raiz:
```code
MYSQL_USER=root
MYSQL_PASSWORD=senha123
MYSQL_DB=diario
SECRET_KEY=sua_chave_secreta

```

## Executando com Docker
```code
docker-compose up --build
```

O backend estará disponível em: `http://localhost:8000/docs` (Swagger UI).
O banco de dados MySQL estará dockerizado e configurado automaticamente.

## API

Endpoints principais (MVP):

POST /auth/register – Cadastrar usuário

POST /auth/login – Login e geração de token JWT

GET /entries – Listar registros do usuário

POST /entries – Criar novo registro

PUT /entries/{id} – Atualizar registro existente

DELETE /entries/{id} – Excluir registro

## Testes

A estrutura de testes está configurada com pytest.

Testes existentes para CRUD de registros em `source/registros/teste_registro.py`.

Um teste skipado apenas para demonstrar funcionamento:

```code
import pytest

@pytest.mark.skip(reason="Teste skipado para entrega MVP")
def test_exemplo_skipado():
    assert True
```

Executar testes:
```code
pytest
```

## Contribuição

Contribuições são bem-vindas! Para manter consistência e boas práticas no projeto, siga as instruções detalhadas no arquivo [CONTRIBUTING.md](CONTRIBUTING.md).

Ele inclui orientações sobre:
* Clonar o repositório
* Criar branch a partir da `main`
* Padrão de commits (**Conventional Commits**)
* Abrir Pull Requests com descrição clara
* Boas práticas de **MVC**, **Clean Code**, **SOLID**, **testes** e **Docker**

Obrigado por ajudar a melhorar o Diário de Enxaqueca!

## Licença

MIT License © [ZenildaVieira]