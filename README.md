# Diário de Enxaqueca - Backend

Backend do projeto **Diário de Enxaqueca**, desenvolvido na disciplina Técnicas de Programação em Plataformas Emergentes (TPPE) da FGA/UnB.

Este módulo contém a API REST principal do sistema, desenvolvida com **FastAPI**, **SQLAlchemy** e **MySQL**, seguindo o padrão **MVC** (Model-View-Controller) com estrutura modular preparada para futura migração para microsserviços.

## Índice

- [Diário de Enxaqueca - Backend](#diário-de-enxaqueca---backend)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
  - [Arquitetura](#arquitetura)
  - [Tecnologias](#tecnologias)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Ambientes](#ambientes)
    - [Desenvolvimento Local](#desenvolvimento-local)
    - [Produção (Railway/Cloud)](#produção-railwaycloud)
  - [Instalação e Configuração](#instalação-e-configuração)
    - [Opção 1: Usando Docker (Recomendado)](#opção-1-usando-docker-recomendado)
    - [Opção 2: Desenvolvimento Local sem Docker](#opção-2-desenvolvimento-local-sem-docker)
  - [Executando com Docker](#executando-com-docker)
  - [API](#api)
    - [Documentação Interativa](#documentação-interativa)
    - [Endpoints Principais](#endpoints-principais)
      - [Episódios](#episódios)
      - [Gatilhos](#gatilhos)
      - [Medicações](#medicações)
      - [Usuários](#usuários)
  - [Testes](#testes)
    - [Executar Testes](#executar-testes)
    - [Estrutura de Testes](#estrutura-de-testes)
    - [Executar Lint](#executar-lint)
  - [Qualidade do Código](#qualidade-do-código)
    - [Métricas Atuais](#métricas-atuais)
    - [Boas Práticas Implementadas](#boas-práticas-implementadas)
  - [Contribuição](#contribuição)
  - [Licença](#licença)

## Visão Geral

O backend fornece uma **API REST completa** para registro e acompanhamento de episódios de enxaqueca, permitindo ao usuário:

- Gerenciar episódios de enxaqueca (CRUD completo) com informações como data, duração, intensidade e sintomas
- Registrar e consultar gatilhos (fatores desencadeantes)
- Gerenciar medicações utilizadas e sua eficácia
- Autenticar usuários via JWT (integração com módulo de autenticação)

A aplicação segue o **padrão MVC**, com código organizado em módulos independentes em `source/`, cada um com suas camadas Model, View (rotas), Controller e Schemas.

## Arquitetura

O backend utiliza **arquitetura MVC modular**, onde cada módulo (episodio, gatilho, medicacao, usuario) possui:

- **Model** (`model_*.py`): Modelos SQLAlchemy (entidades do banco de dados)
- **View** (`view_*.py`): Rotas FastAPI (endpoints da API)
- **Controller** (`controller_*.py`): Lógica de negócio
- **Schemas** (`schemas_*.py`): Validação de dados com Pydantic V2
- **Tests** (`test_*.py`, `test_integration_*.py`): Testes unitários e de integração

Esta estrutura modular facilita a manutenção e permite futura extração de módulos para microsserviços independentes.

## Tecnologias

- **Python 3.11.14**
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM para manipulação do banco de dados
- **Pydantic V2** - Validação de dados e serialização
- **MySQL 8** - Banco de dados relacional
- **JWT** - Autenticação via tokens (integração com módulo auth)
- **pytest** - Framework de testes (cobertura de 95%)
- **Pylint** - Análise estática de código (nota 9.60/10)
- **Docker & Docker Compose** - Containerização

## Estrutura do Projeto

```
backend/
├── config/
│   ├── database.py          # Configuração do banco de dados
│   └── settings.py          # Configurações gerais
├── mysql-init/
│   └── init.sql             # Script de inicialização do MySQL
├── source/
│   ├── episodio/            # Módulo de episódios
│   │   ├── model_episodio.py
│   │   ├── view_episodio.py
│   │   ├── controller_episodio.py
│   │   ├── schemas_episodio.py
│   │   ├── test_episodio.py
│   │   └── test_integration_episodio.py
│   ├── gatilho/             # Módulo de gatilhos
│   │   ├── model_gatilho.py
│   │   ├── view_gatilho.py
│   │   ├── controller_gatilho.py
│   │   ├── schemas_gatilho.py
│   │   ├── test_gatilho.py
│   │   └── test_integration_gatilho.py
│   ├── medicacao/           # Módulo de medicações
│   │   ├── model_medicacao.py
│   │   ├── view_medicacao.py
│   │   ├── controller_medicacao.py
│   │   ├── schemas_medicacao.py
│   │   ├── test_medicacao.py
│   │   └── test_integration_medicacao.py
│   └── usuario/             # Módulo de usuários
│       ├── model_usuario.py
│       ├── view_usuario.py
│       ├── controller_usuario.py
│       ├── schemas_usuario.py
│       ├── test_usuario.py
│       └── test_integration_usuario.py
├── htmlcov/                 # Relatórios de cobertura de testes
├── main.py                  # Ponto de entrada da aplicação
├── conftest.py              # Configurações do pytest
├── pytest.ini               # Configurações do pytest
├── requirements.txt         # Dependências Python
├── Dockerfile               # Build do container
├── wait-for-db.sh          # Script de espera do MySQL
├── CONTRIBUTING.md          # Guia de contribuição
├── LICENSE
└── README.md
```

## Ambientes

### Desenvolvimento Local

**Configuração via Docker Compose:**

```env
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=diario_user
MYSQL_PASSWORD=********
MYSQL_DB=diario_enxaqueca
MYSQL_USE_SSL=false
SECRET_KEY=dev-secret-key-change-in-production
ENVIRONMENT=development
DEBUG=true
```

**Acesso:**
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### Produção (Aiven Cloud)

**Configuração com banco gerenciado Aiven:**

```env
MYSQL_HOST=mysql-2e80f044-diario-de-enxaqueca.k.aivencloud.com
MYSQL_PORT=24445
MYSQL_USER=avnadmin
MYSQL_PASSWORD=********
MYSQL_DB=defaultdb
MYSQL_SSL=True
MYSQL_SSL_CA=/app/ca.pem
SECRET_KEY=your-production-secret-key-here
ENVIRONMENT=production
DEBUG=false
```

**Características:**
- Banco de dados MySQL gerenciado no Aiven Cloud
- SSL/TLS obrigatório para conexões (certificado ca.pem)
- Logs estruturados
- Variáveis de ambiente injetadas pelo provedor cloud
- Health checks configurados

## Instalação e Configuração

### Opção 1: Usando Docker (Recomendado)

Na raiz do projeto (não na pasta backend):

```bash
# Subir todos os serviços (backend, auth, db, frontend)
docker-compose up --build -d

# Ver logs do backend
docker-compose logs -f backend

# Verificar status
docker-compose ps
```

### Opção 2: Desenvolvimento Local sem Docker

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar .env (ajustar MYSQL_HOST para localhost)
cp ../.env .env

# Executar aplicação
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Nota:** Certifique-se de ter um MySQL rodando e acessível em localhost:3306.

## Executando com Docker

O backend está totalmente containerizado e orquestrado via Docker Compose:

```bash
# Build e start
docker-compose up backend --build -d

# Apenas backend + banco de dados
docker-compose up db backend -d

# Ver logs
docker-compose logs -f backend

# Parar serviço
docker-compose stop backend

# Remover container
docker-compose down
```

## API

### Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principais

#### Episódios
- `GET /api/episodios` - Listar episódios do usuário autenticado
- `POST /api/episodios` - Criar novo episódio
- `GET /api/episodios/{id}` - Obter episódio específico
- `PUT /api/episodios/{id}` - Atualizar episódio
- `DELETE /api/episodios/{id}` - Excluir episódio

#### Gatilhos
- `GET /api/gatilhos` - Listar gatilhos do usuário
- `POST /api/gatilhos` - Criar gatilho
- `GET /api/gatilhos/{id}` - Obter gatilho específico
- `PUT /api/gatilhos/{id}` - Atualizar gatilho
- `DELETE /api/gatilhos/{id}` - Excluir gatilho

#### Medicações
- `GET /api/medicacoes` - Listar medicações do usuário
- `POST /api/medicacoes` - Criar medicação
- `GET /api/medicacoes/{id}` - Obter medicação específica
- `PUT /api/medicacoes/{id}` - Atualizar medicação
- `DELETE /api/medicacoes/{id}` - Excluir medicação

#### Usuários
- `GET /api/usuarios/me` - Obter dados do usuário autenticado
- `PUT /api/usuarios/{id}` - Atualizar dados do usuário
- `DELETE /api/usuarios/{id}` - Excluir conta

**Nota:** A autenticação (login/registro) está no módulo `autenticacao` separado.

## Testes

O backend possui **95% de cobertura** com testes unitários e de integração.

### Executar Testes

```bash
# Via Docker (recomendado)
docker-compose run --rm tests

# Com relatório de cobertura
docker-compose run --rm tests pytest --cov=source --cov-report=html

# Ver relatório HTML
# Abra backend/htmlcov/index.html no navegador

# Localmente (sem Docker)
cd backend
pytest
pytest --cov=source --cov-report=term-missing
```

### Estrutura de Testes

- **Testes Unitários** (`test_*.py`): Testam lógica de negócio isoladamente
- **Testes de Integração** (`test_integration_*.py`): Testam endpoints completos com banco de dados em memória (SQLite)

### Executar Lint

```bash
# Via Docker
docker-compose run --rm lint pylint --rcfile=../.pylintrc source/*/*.py

# Localmente
pylint --rcfile=../.pylintrc source/*/*.py
```

## Qualidade do Código

### Métricas Atuais

- **Cobertura de Testes**: 95%
- **Pylint Score**: 9.60/10
- **Testes Passing**: 34/34 (100%)
- **Pydantic**: V2 (latest)

### Boas Práticas Implementadas

- Padrão MVC modular
- Validação de dados com Pydantic V2
- Testes unitários e de integração
- Análise estática de código (Pylint)
- Documentação automática (Swagger/OpenAPI)
- Type hints em todo o código
- Separação clara de responsabilidades
- Containerização completa

## Contribuição

Contribuições são bem-vindas! Para manter consistência e boas práticas no projeto, siga as instruções detalhadas no arquivo [CONTRIBUTING.md](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/backend/CONTRIBUTING.md).

Orientações incluem:
- Clonar o repositório e configurar ambiente
- Criar branch a partir da `main`
- Padrão de commits (**Conventional Commits**)
- Executar testes antes de abrir PR
- Manter cobertura acima de 90%
- Seguir padrão MVC e Clean Code

## Licença

MIT License © [ZenildaVieira](https://github.com/ZenildaVieira)