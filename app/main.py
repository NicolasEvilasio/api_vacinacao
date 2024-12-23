"""
Application entry point.

This is the main FastAPI application module.
It is responsible for:
- Initializing the application
- Configuring middlewares
- Registering routes
- Managing application lifecycle

Here all parts of the application are united in a single entry point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import database
from app.controllers import (
    countries, 
    states,
    cities,
    vaccination_points,
    vaccines
)
from app.config import limiter, logger, settings
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Connecting to the database...")
        await database.connect()
        logger.info("Connection established successfully!")
        yield
    finally:
        logger.info("Disconnecting from the database...")
        await database.disconnect()
        logger.info("Connection closed!")

app = FastAPI(
    title="API de Vacinação",
    description="""
    API para gerenciamento de dados de vacinação no Brasil.
    
    Funcionalidades principais:
    * Gerenciamento de locais (países, estados, cidades)
    * Gerenciamento de pontos de vacinação
    * Gerenciamento de vacinas disponíveis
    * Relacionamento entre pontos de vacinação e vacinas
    
    Todos os endpoints possuem rate limiting de 10 requisições por minuto.
    
    Todos os dados são fictícios.
    """,
    version="1.1.0",
    lifespan=lifespan,
    servers=[
        {
            "url": settings.PRODUCTION_URL,
            "description": "Production Server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Local Development Server"
        }
    ],
    openapi_tags=[
        {
            "name": "Países",
            "description": "Gerenciamento de países"
        },
        {
            "name": "Estados",
            "description": "Gerenciamento de estados"
        },
        {
            "name": "Cidades",
            "description": "Gerenciamento de cidades"
        },
        {
            "name": "Pontos de Vacinação",
            "description": "Gerenciamento de pontos de vacinação"
        },
        {
            "name": "Vacinas",
            "description": "Gerenciamento de vacinas"
        }
    ]
)

# Rate limiter configuration
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routes
app.include_router(countries.router)
app.include_router(states.router)
app.include_router(cities.router)
app.include_router(vaccination_points.router)
app.include_router(vaccines.router)
