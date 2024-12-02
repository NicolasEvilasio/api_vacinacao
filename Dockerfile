# Use uma imagem base com Python
FROM python:3.10-slim

# Defina o diretório de trabalho
WORKDIR /app

# Instale as dependências do Poetry
RUN pip install poetry

# Copie o arquivo pyproject.toml e poetry.lock
COPY pyproject.toml poetry.lock /app/

# Instale as dependências do projeto
RUN poetry install --no-dev

# Copie o código da aplicação
COPY . /app/

# Exponha a porta que a aplicação usará
EXPOSE 8000

# Inicializar banco e executar aplicação
CMD poetry run python -m app.init_db && \
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
