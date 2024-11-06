"""
Ponto de entrada da aplicação.

Este é o módulo principal da aplicação FastAPI.
É responsável por:
- Inicializar a aplicação
- Configurar middlewares
- Registrar rotas
- Gerenciar o ciclo de vida da aplicação

Aqui são unidas todas as partes da aplicação em um único ponto de entrada.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import database
from app.controllers import example_controller
from app.config import limiter, logger
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Conectando ao banco de dados...")
        await database.connect()
        logger.info("Conexão estabelecida com sucesso!")
        yield
    finally:
        logger.info("Desconectando do banco de dados...")
        await database.disconnect()
        logger.info("Conexão encerrada!")

app = FastAPI(
    title="API de Vacinação",
    description="API para gerenciamento de dados de vacinação",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração do rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Rotas
app.include_router(example_controller.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World!"}
