"""
This module contains the controllers (route handlers) for the Countries resource.
The controllers are responsible for:
- Receiving HTTP requests
- Validating input data
- Calling appropriate services
- Returning formatted HTTP responses

Controllers should not contain business logic, only HTTP request 
handling logic.
"""

from fastapi import APIRouter, Depends, Request, Form, Query
from typing import Annotated
from app.schemas.countries import CountryCreate
from app.services.countries import CountryService
from app.dependencies import get_country_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/countries",
    tags=["Países"],
    summary="Listar países",
    description="""
    Retorna todos os países cadastrados.
    
    É possível filtrar por:
    * ID do país
    * Código IBGE do país
    
    Se nenhum filtro for fornecido, retorna todos os países.
    """,
    response_description="Lista de países encontrados",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "Brasil",
                        "ibge_code": "1058",
                        "created_at": "2024-01-01T00:00:00"
                    }]
                }
            }
        },
        429: {
            "description": "Muitas requisições - Aguarde antes de tentar novamente"
        }
    }
)
@limiter.limit("10/minute")
async def get_countries(
    request: Request,
    id: int | None = Query(None, description="ID do país"),
    ibge_code: str | None = Query(None, description="Código IBGE do país"),
    service: CountryService = Depends(get_country_service)
):
    return await service.get_all_countries(id=id, ibge_code=ibge_code)

@router.post(
    "/countries",
    tags=["Países"],
    summary="Cadastrar um país",
    description="Cadastra um novo país no sistema",
    response_description="País criado com sucesso",
    status_code=201,
    responses={
        201: {
            "description": "País criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "message": "País criado com sucesso"
                    }
                }
            }
        },
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "name"],
                                "msg": "O nome do país é obrigatório",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def create_country(
    country: CountryCreate,
    service: CountryService = Depends(get_country_service)
):
    return await service.create_country(country)