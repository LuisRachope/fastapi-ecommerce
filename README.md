# FastAPI E-commerce

API REST moderna para gerenciamento de e-commerce construída com FastAPI, seguindo arquitetura limpa e princípios SOLID.

## 🎯 Visão Geral

Projeto de referência implementando padrões consolidados de mercado:
- **Clean Architecture**: Separação clara de responsabilidades entre camadas
- **Repository Pattern**: Abstração da camada de persistência
- **Dependency Injection**: Inversão de controle para maior testabilidade
- **SOLID Principles**: Código escalável e manutenível

## 🚀 Tecnologias

- **FastAPI** 0.104.1 - Framework web assíncrono
- **SQLAlchemy** 2.0.23 - ORM com suporte a async
- **Pydantic** 2.5.2 - Validação de dados com type hints
- **Uvicorn** 0.24.0 - ASGI server
- **SQLite** - Banco de dados (com aiosqlite 0.19.0)
- **JWT** com **PyJWT** 2.8.0 - Autenticação segura
- **Bcrypt** 4.0.1 - Hash de senhas
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
├── main.py                          # Ponto de entrada da aplicação
├── presentation/                    # Camada de apresentação (controllers e schemas)
│   ├── api/v1/endpoints/           # Rotas da API
│   │   ├── auth_handler.py         # Endpoints de autenticação
│   │   ├── product_handler.py      # Endpoints de produtos
│   │   ├── order_handler.py        # Endpoints de pedidos
│   │   └── ping_handler.py         # Health check
│   └── schemas/                     # Schemas Pydantic para validação
├── application/                     # Camada de aplicação (lógica de negócio)
│   ├── use_cases/                  # Casos de uso
│   │   ├── auth_use_case.py
│   │   ├── product_use_case.py
│   │   └── order_use_case.py
│   ├── services/                   # Serviços de aplicação (deprecated)
│   └── dtos/                       # Data Transfer Objects
├── domain/                          # Camada de domínio (entidades e interfaces)
│   ├── entities/                   # Entidades de domínio
│   ├── enums/                      # Enumerações (ex: OrderStatus)
│   └── repositories/               # Interfaces de repositório
├── infrastructure/                  # Camada de infraestrutura
│   ├── persistence/
│   │   ├── models/                 # Modelos ORM SQLAlchemy
│   │   └── repositories/           # Implementações dos repositórios
│   └── converters.py               # Conversão entre modelos e entidades
├── core/                            # Núcleo da aplicação
│   ├── config.py                   # Configurações (settings)
│   ├── database.py                 # Inicialização do banco
│   ├── dependencies.py             # Injeção de dependências
│   ├── exceptions.py               # Exceções customizadas
│   ├── security.py                 # Autenticação JWT
│   ├── request_context.py          # Contexto da requisição
│   ├── logging_config.py           # Configuração de logs
│   └── utils.py                    # Utilitários
└── tests/                           # Suite de testes
    └── unit/
        ├── repositories/           # Testes de repositórios
        └── services/               # Testes de serviços
```

### Padrões Arquiteturais

- **Clean Architecture**: Separação em camadas independentes
- **Repository Pattern**: Abstração de acesso a dados
- **Dependency Injection**: Container de dependências configurável
- **Use Cases**: Lógica de negócio isolada
- **DTOs**: Transfer de dados entre camadas
- **SOLID Principles**: Código escalável e manutenível

## 🧪 Testes

Execute os testes:

```bash
pytest
```

Com cobertura de código:

```bash
pytest --cov=app --cov-report=html
```

Executar testes específicos:

```bash
pytest tests/unit/repositories/     # Testes de repositórios
pytest tests/unit/services/         # Testes de serviços
pytest -v                           # Verbose mode
```

## 📊 Modelo de Dados

### User (Usuário)

```python
{
  "id": int,
  "email": str,
  "password_hash": str,
  "is_superuser": bool,
  "created_at": datetime
}
```

### Product (Produto)

```python
{
  "id": int,
  "name": str,
  "description": str,
  "price": float,  # Decimal
  "quantity": int,
  "created_at": datetime,
  "updated_at": datetime
}
```

### Order (Pedido)

```python
{
  "id": int,
  "user_id": int,
  "order_date": datetime,
  "status": str,  # OrderStatus enum
  "total_amount": float,  # Decimal
  "items": [OrderItem],
  "created_at": datetime
}
```

### OrderItem (Item do Pedido)

```python
{
  "id": int,
  "order_id": int,
  "product_id": int,
  "quantity": int,
  "price": float  # Preço no momento da compra
}
```

## 🛠️ Comandos Úteis

### Makefile commands

```bash
make execute      # Executa a aplicação
make test         # Roda os testes
make lint         # Executa linter
make format       # Formata o código
```

### Desenvolvimento com Uvicorn

```bash
# Com reload automático
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## 🔄 Fluxo de Exemplo

1. **Registrar usuário**:
   ```bash
   POST /auth/register
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "senha123"
   }
   ```

2. **Fazer login**:
   ```bash
   POST /auth/login
   Content-Type: application/x-www-form-urlencoded

   username=user@example.com&password=senha123
   ```

3. **Criar produto** (com token):
   ```bash
   POST /products
   Authorization: Bearer {token}
   Content-Type: application/json

   {
     "name": "Produto A",
     "description": "Descrição",
     "price": 99.99,
     "quantity": 10
   }
   ```

4. **Criar pedido** (com token):
   ```bash
   POST /orders/create
   Authorization: Bearer {token}
   Content-Type: application/json

   {
     "items": [
       {
         "product_id": 1,
         "quantity": 2
       }
     ]
   }
   ```

## 🚨 Tratamento de Erros

A API retorna erros com estrutura padronizada:

```json
{
  "detail": "Descrição do erro"
}
```

E códigos HTTP apropriados (400, 401, 403, 404, 500, etc.)

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` com as seguintes variáveis (opcional, possui defaults):

```env
DATABASE_URL=sqlite+aiosqlite:///./ecommerce.db
API_TITLE=FastAPI E-commerce
API_VERSION=1.0.0
API_DESCRIPTION=API REST para gerenciamento de e-commerce
DOCS_URL=/docs
REDOC_URL=/redoc
```

## 📌 Endpoints Principais

### 🏥 Health Check

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/ping` | Health check da API |

### 🔐 Autenticação (`/auth`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/register` | Registrar novo usuário |
| POST | `/auth/login` | Login com email/senha (form data) |
| POST | `/auth/login/json` | Login com JSON |
| GET | `/auth/me` | Obter dados do usuário atual |
| GET | `/auth/users` | Listar todos os usuários |

### 📦 Produtos (`/products`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/products` | Criar novo produto |
| GET | `/products` | Listar produtos com paginação |
| GET | `/products/{product_id}` | Obter produto por ID |
| PATCH | `/products/{product_id}` | Atualizar produto |
| DELETE | `/products/{product_id}` | Deletar produto |

### 🛒 Pedidos (`/orders`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/orders/create` | Criar novo pedido |
| GET | `/orders` | Listar todos os pedidos |
| DELETE | `/orders/{order_id}` | Deletar pedido |

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação segura.

### Fluxo de Autenticação

1. **Registrar usuário**: POST `/auth/register`
2. **Login**: POST `/auth/login` (retorna access_token)
3. **Usar token**: Adicione header `Authorization: Bearer {token}` nas requisições autenticadas

### Exemplo de Login

```bash
curl -X POST "http://localhost:8080/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=seu@email.com&password=sua_senha"
```

### Usar Token Protegido

```bash
curl -X GET "http://localhost:8080/auth/me" \
  -H "Authorization: Bearer {seu_access_token}"
```
