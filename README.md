# FastAPI E-commerce

API REST moderna para gerenciamento de e-commerce construída com FastAPI, seguindo arquitetura limpa e princípios SOLID.

## 🎯 Visão Geral

Projeto de referência implementando padrões consolidados de mercado:
- **Clean Architecture**: Separação clara de responsabilidades entre camadas
- **Repository Pattern**: Abstração da camada de persistência
- **Dependency Injection**: Inversão de controle para maior testabilidade
- **SOLID Principles**: Código escalável e manutenível

## 🚀 Tecnologias

- **FastAPI** 0.104+ - Framework web assíncrono
- **SQLAlchemy** 2.0+ - ORM com suporte a async
- **Pydantic** 2.5+ - Validação de dados e settings
- **Pytest** 7.4+ - Suite de testes com cobertura

## 📋 Pré-requisitos

- Python 3.10+
- pip ou gerenciador de pacotes similar

## 🔧 Instalação

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///./test.db
API_TITLE=FastAPI E-commerce
API_VERSION=1.0.0
API_DESCRIPTION=API REST para gerenciamento de e-commerce
DOCS_URL=/docs
REDOC_URL=/redoc
```

## ▶️ Executando a Aplicação

### Com MakeFile (recomendado)

```bash
make execute
```

### Diretamente com Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

A API estará disponível em [http://localhost:8080](http://localhost:8080/ui)

### Acessar a Documentação

Após iniciar a aplicação, acesse:

- **Swagger UI (Interactive)**: [http://localhost:8080/ui](http://localhost:8080/ui)

## 📁 Estrutura do Projeto

```
app/
├── presentation/      # Camada de apresentação (controllers, schemas)
├── application/       # Regras de negócio (services, DTOs)
├── domain/            # Entidades e interfaces de repositório
├── infrastructure/    # Implementações de repositório e ORM
├── core/              # Configurações, exceções e utilitários
└── tests/             # Suite de testes
```

## 🧪 Testes

Execute os testes:

```bash
pytest
```

Com cobertura:

```bash
pytest --cov=app --cov-report=html
```

Executar por marcador:

```bash
pytest -m unit        # Testes unitários
pytest -m integration # Testes de integração
```

## 📌 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/ping` | Health check da API |
| GET | `/v1/products` | Listar produtos |
| POST | `/v1/products` | Criar produto |
