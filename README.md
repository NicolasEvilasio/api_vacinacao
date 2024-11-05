# API de Vacinação

API desenvolvida em FastAPI para gerenciamento de vacinação, utilizando PostgreSQL no Tembo Cloud.

## Tecnologias Utilizadas

- Python 3.10
- FastAPI
- PostgreSQL
- SQLAlchemy
- Poetry
- Docker

## Pré-requisitos

- Python 3.10+
- Poetry
- Docker (opcional)

## Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/api_vacinacao.git
cd api_vacinacao
```

2. Instale as dependências com Poetry:
```bash
poetry install
```	

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
DB_USERNAME=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=seu_host
DB_PORT=5432
DB_NAME=seu_banco_de_dados
ENVIRONMENT=development
```

4. Execute o comando para criar as tabelas no banco de dados:
```bash
poetry run python -m app.init_db
```

## 🚀 Executando a API

1. Execute o comando para rodar o servidor dev da API:
```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação

Acesse a documentação interativa da API em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛣️ Endpoints

### Root
- GET `/`: Endpoint raiz que retorna uma mensagem de boas-vindas

### Examples
- GET `/examples`: Lista todos os exemplos cadastrados
- POST `/examples/`: Cria um novo exemplo

## ⚙️ Configurações

- Rate Limiting: 10 requisições por minuto
- Logging configurado para nível INFO
- Validação de dados com Pydantic
- Conexão assíncrona com PostgreSQL

## 👤 Autor

Nicolas Evilasio
- Email: nicolas_evilasio@hotmail.com

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.