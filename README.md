# API de Vacinação

API para gerenciamento de dados de vacinação no Brasil.

## Funcionalidades

* Gerenciamento de locais (países, estados, cidades)
* Gerenciamento de pontos de vacinação
* Gerenciamento de vacinas disponíveis
* Relacionamento entre pontos de vacinação e vacinas

## Tecnologias

* Python 3.10+
* Poetry
* Docker
* FastAPI
* SQLAlchemy
* PostgreSQL/SQLite

## Configuração

1. Clone o repositório:

```bash
git clone https://github.com/NicolasEvilasio/api_vacinacao.git
cd api_vacinacao
```

2. Instale as dependências com Poetry:
```bash
poetry install
```	

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

#### Configuração do banco de dados SQLite
```bash
SQLITE_DB_NAME=database.db
DATABASE_TYPE=sqlite
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

## ⚙️ Configurações

- Rate Limiting: 10 requisições por minuto
- Logging configurado para nível INFO
- Validação de dados com Pydantic

## 👤 Autor

Nicolas Evilasio
- Email: nicolas_evilasio@hotmail.com

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.