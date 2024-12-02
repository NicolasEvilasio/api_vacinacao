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

from fastapi import APIRouter, Depends, Request, Form, Query
from typing import Annotated
from app.schemas.cities import CityCreate
from app.services.cities import CityService
from app.dependencies import get_city_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/cities",
    tags=["Cidades"],
    summary="Listar cidades",
    description="""
    Retorna a lista de cidades cadastradas.
    
    Filtros disponíveis:
    * ID da cidade
    * Nome da cidade (busca parcial, não sensível a maiúsculas/minúsculas)
    * Código IBGE
    
    Se nenhum filtro for fornecido, retorna todas as cidades.
    """,
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
    description="Cadastra uma cidade"
)
async def create_city(
    city: CityCreate,
    service: CityService = Depends(get_city_service)
):
    return await service.create_city(city)