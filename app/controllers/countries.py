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

from fastapi import APIRouter, Depends, Request, Query
from app.schemas.countries import CountryCreate, CountryUpdate
from app.services.countries import CountryService
from app.dependencies import get_country_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/countries",
    tags=["Países"],
    summary="Listar países",
    description="""Retorna a lista de países cadastrados.""",
    response_description="Lista de países"
)
@limiter.limit("10/minute")
async def get_countries(
    request: Request,
    id: int | None = Query(None, description="ID do país"),
    name: str | None = Query(None, description="Nome do país (busca parcial)"),
    ibge_code: str | None = Query(None, description="Código IBGE do país"),
    service: CountryService = Depends(get_country_service)
):
    return await service.get_all_countries(id=id, name=name, ibge_code=ibge_code)

@router.post(
    "/countries",
    tags=["Países"],
    summary="Cadastrar um país",
    description="Cadastra um novo país no sistema",
    response_description="País criado com sucesso",
    status_code=201
)
async def create_country(
    country: CountryCreate,
    service: CountryService = Depends(get_country_service)
):
    return await service.create_country(country)

@router.patch(
    "/countries/{id}",
    tags=["Países"],
    summary="Atualizar um país",
    description="Atualiza parcialmente os dados de um país específico",
    response_description="País atualizado com sucesso",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "País atualizado com sucesso"
                    }
                }
            }
        },
        404: {
            "description": "País não encontrado"
        }
    }
)
async def update_country(
    id: int,
    country: CountryUpdate,
    service: CountryService = Depends(get_country_service)
):
    return await service.update_country(id, country)

@router.delete(
    "/countries/{id}",
    tags=["Países"],
    summary="Excluir um país",
    description="Remove um país do sistema",
    response_description="País excluído com sucesso",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "País excluído com sucesso"
                    }
                }
            }
        },
        404: {
            "description": "País não encontrado"
        }
    }
)
async def delete_country(
    id: int,
    service: CountryService = Depends(get_country_service)
):
    return await service.delete_country(id)