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

O projeto tem como objetivo fornecer **uma aplicação CRUD** para registro e acompanhamento de episódios de enxaqueca, permitindo ao usuário:
* Criar episódios de enxaqueca com informações como intensidade, gatilhos, medicação e observações.
* Consultar, atualizar e excluir espisódios existentes.
* Testar a funcionalidade de forma estruturada utilizando testes automatizados.

A aplicação segue o **padrão MVC**, com código organizado em `source/` e subpastas para cada regra de negócio.

## Primeira Entrega

Para a primeira entrega, o MVP contempla:

Cadastro de **episódios de enxaqueca** (CRUD completo).

Backend funcional com **FastAPI**, **MySQL** via **SQLAlchemy**.

Estrutura de testes básica, com pelo **um teste skipado** para demonstrar a configuração de testes.

Preparação para integração futura com frontend em **React.js + TypeScript**.

## Backlog

Lista de 10 histórias de usuário simplificadas para o MVP: [backlog.md](https://github.com/diario-enxaqueca/documentacao/blob/main/docs/backlog.md)

## Tecnologias

* Linguagem: Python 3.10+
* Framework: FastAPI
* Banco de Dados: MySQL (dockerizado)
* ORM: SQLAlchemy
* Documentação da API: Swagger (a ser implementado)
* Testes: Pytest (para a primeira entrega apenas um teste skipado)
* Docker & Docker Compose
* Padrões de código: Clean Code, SOLID, Lint

## Estrutura do Projeto
```code
backend/
│
├── mysql-init/
│   ├── init.sql                    # 
├── source/
│   ├── episodio/                   # a ser implementado
│   │   ├── model_episodio.py
│   │   ├── view_episodio.py
│   │   ├── controller_episodio.py
│   │   └── teste_episodio.py
│   ├── dashboard/                  # a ser implementado
│   │   ├── model_episodio.py
│   │   ├── view_episodio.py
│   │   ├── controller_episodio.py
│   │   └── teste_episodio.py
│   ├── gatilho/                    # a ser implementado
│   │   ├── model_episodio.py
│   │   ├── view_episodio.py
│   │   ├── controller_episodio.py
│   │   └── teste_episodio.py
│   ├── medicacao/                  # a ser implementado
│   │   ├── model_episodio.py
│   │   ├── view_episodio.py
│   │   ├── controller_episodio.py
│   │   └── teste_episodio.py
│   ├── usuario/                    # a ser implementado
│   │   ├── model_usuario.py
│   │   ├── view_usuario.py
│   │   ├── controller_usuario.py
│   │   └── teste_usuario.py
│   └── teste_db.py                 # a ser implementado
├── main.py                         # Chama as rotas
├── config.py                       # Configurações do projeto
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── wait-for-db.sh
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Instalação e Configuração

Clone o repositório:
```code
git clone https://github.com/diario-enxaqueca/backend.git
cd backend
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

GET /entries – Listar episódios de enxaqueca do usuário

POST /entries – Criar novo episódio de enxaqueca

PUT /entries/{id} – Atualizar episódio de enxaqueca existente

DELETE /entries/{id} – Excluir episódio de enxaqueca salvo

## Testes

A estrutura de testes está configurada com pytest.

Testes existentes para CRUD de episódios em `source/episodio/teste_episodio.py`.

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

Executar Lint:
```code
ruff check .
```

Para corrigir automaticamente:
```code
ruff check . --fix
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