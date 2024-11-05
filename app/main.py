from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from app.database import database
from app.models import Example
from sqlalchemy import select, insert
from pydantic import BaseModel, Field
from typing import Optional
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

logging.getLogger("databases").setLevel(logging.WARNING)


class ExampleCreate(BaseModel):
    name: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9 ]*$",
        description="Nome do exemplo",
        example="Jabulani"
    )
    description: Optional[str] = Field(
        None, 
        description="Descrição detalhada do exemplo",
        example="Bola de futebol utilizada na Copa do Mundo de 2010"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jabulani",
                "description": "Bola de futebol utilizada na Copa do Mundo de 2010"
            }
        }

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

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="API de Vacinação",
    description="API para gerenciamento de dados de vacinação",
    version="1.0.0",
    contact={
        "name": "Nicolas Evilasio",
        "email": "nicolas_evilasio@hotmail.com"
    },
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Retorna uma mensagem de boas-vindas"
)
async def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    """
    return {"message": "Hello World!"}

@app.get(
    "/examples",
    tags=["Examples"],
    summary="Listar exemplos",
    description="Retorna todos os exemplos cadastrados no banco de dados",
    response_description="Lista de exemplos encontrados"
)
@limiter.limit("10/minute")
async def get_examples(request: Request):
    """
    Retorna uma lista com todos os exemplos cadastrados no banco de dados.
    """
    query = select(Example)
    return await database.fetch_all(query)

@app.post(
    "/examples/",
    tags=["Examples"],
    summary="Criar exemplo",
    description="Cria um novo exemplo no banco de dados",
    response_description="Exemplo criado com sucesso"
)
async def create_example(example: ExampleCreate):
    """
    Cria um novo exemplo com os dados fornecidos.

    - **name**: Nome do exemplo (obrigatório)
    - **description**: Descrição do exemplo (opcional)
    """
    query = insert(Example).values(
        name=example.name,
        description=example.description
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "message": "Registro criado com sucesso"}
