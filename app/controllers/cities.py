"""
This module contains the controllers (route handlers) for the Cities resource.
The controllers are responsible for:
- Receiving HTTP requests
- Validating input data
- Calling appropriate services
- Returning formatted HTTP responses

Controllers should not contain business logic, only HTTP request 
handling logic.
"""

from fastapi import APIRouter, Depends, Request, Query
from app.models import City
from app.schemas.cities import CityCreate, CityUpdate
from app.services.cities import CityService
from app.dependencies import get_city_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/cities",
    tags=["Cidades"],
    summary="Listar cidades",
    description="""Retorna a lista de cidades cadastradas.""",
    response_description="Lista de cidades"
)
@limiter.limit("10/minute")
async def get_cities(
    request: Request,
    id: int | None = Query(None, description="ID da cidade"),
    name: str | None = Query(None, description="Nome da cidade (busca parcial)"),
    ibge_code: str | None = Query(None, description="Código IBGE da cidade"),
    service: CityService = Depends(get_city_service)
):
    return await service.get_all_cities(id=id, name=name, ibge_code=ibge_code)

@router.post(
    "/cities",
    tags=["Cidades"],
    summary="Cadastrar uma cidade",
    description="Cadastra uma nova cidade no sistema",
    response_description="Cidade criada com sucesso",
    status_code=201
)
async def create_city(
    city: CityCreate,
    service: CityService = Depends(get_city_service)
):
    return await service.create_city(city)

@router.patch(
    "/cities/{id}",
    tags=["Cidades"],
    summary="Atualizar uma cidade",
    description="Atualiza parcialmente os dados de uma cidade específica",
    response_description="Cidade atualizada com sucesso",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Cidade atualizada com sucesso"
                    }
                }
            }
        },
        404: {
            "description": "Cidade não encontrada"
        }
    }
)
async def update_city(
    id: int,
    city: CityUpdate,
    service: CityService = Depends(get_city_service)
):
    return await service.update_city(id, city)

@router.delete(
    "/cities/{id}",
    tags=["Cidades"],
    summary="Excluir uma cidade",
    description="Remove uma cidade do sistema",
    response_description="Cidade excluída com sucesso",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Cidade excluída com sucesso"
                    }
                }
            }
        },
        404: {
            "description": "Cidade não encontrada"
        }
    }
)
async def delete_city(
    id: int,
    service: CityService = Depends(get_city_service)
):
    return await service.delete_city(id)