"""
This module contains the controllers (route handlers) for the VaccinationPoints resource.
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
from app.schemas.vaccination_points import VaccinationPointCreate
from app.services.vaccination_points import VaccinationPointService
from app.services.vaccination_point_vaccines import VaccinationPointVaccineService
from app.dependencies import get_vaccination_point_service, get_vaccination_point_vaccine_service
from app.config import limiter
from app.schemas.vaccination_point_vaccines import VaccinationPointVaccineCreate

router = APIRouter()

@router.get(
    "/vaccination-points",
    tags=["Pontos de Vacinação"],
    summary="Listar pontos de vacinação",
    description="""
    Retorna a lista de pontos de vacinação cadastrados.
    
    Filtros disponíveis:
    * ID do ponto de vacinação
    * Nome do ponto (busca parcial, não sensível a maiúsculas/minúsculas)
    * Cidade (ID)
    
    Se nenhum filtro for fornecido, retorna todos os pontos de vacinação.
    """,
    response_description="Lista de pontos de vacinação"
)
@limiter.limit("10/minute")
async def get_vaccination_points(
    request: Request,
    id: int | None = Query(None, description="ID do ponto de vacinação"),
    name: str | None = Query(None, description="Nome do ponto de vacinação (busca parcial)"),
    city_id: int | None = Query(None, description="ID da cidade"),
    service: VaccinationPointService = Depends(get_vaccination_point_service)
):
    return await service.get_all_vaccination_points(id=id, name=name, city_id=city_id)

@router.post(
    "/vaccination-points",
    tags=["Pontos de Vacinação"],
    summary="Cadastrar um ponto de vacinação",
    description="Cadastra um ponto de vacinação"
)
async def create_vaccination_point(
    vaccination_point: VaccinationPointCreate,
    service: VaccinationPointService = Depends(get_vaccination_point_service)
):
    return await service.create_vaccination_point(vaccination_point)

@router.get(
    "/vaccination-points/vaccines",
    tags=["Pontos de Vacinação"],
    summary="Listar vacinas por ponto de vacinação",
    description="""
    Retorna a lista de vacinas disponíveis em cada ponto de vacinação.
    
    Se um vaccination_point_id for fornecido, retorna apenas as vacinas daquele ponto específico.
    Caso contrário, retorna as vacinas de todos os pontos.
    """,
    response_description="Lista de pontos de vacinação com suas vacinas",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": [{
                        "vaccination_point_id": 1,
                        "vaccination_point_name": "Centro de Vacinação Ponta Verde",
                        "vaccines": [
                            {
                                "id": 1,
                                "name": "BCG"
                            },
                            {
                                "id": 2,
                                "name": "Hepatite B"
                            }
                        ]
                    }]
                }
            }
        }
    }
)
@limiter.limit("10/minute")
async def get_vaccines_by_point(
    request: Request,
    vaccination_point_id: int | None = Query(None, description="ID do ponto de vacinação"),
    service: VaccinationPointVaccineService = Depends(get_vaccination_point_vaccine_service)
):
    return await service.get_vaccines_by_point(vaccination_point_id)

@router.get(
    "/vaccination-points/by-vaccine",
    tags=["Pontos de Vacinação"],
    summary="Listar pontos de vacinação por vacina",
    description="""
    Retorna a lista de pontos de vacinação que oferecem determinada vacina.
    
    Se um vaccine_id for fornecido, retorna apenas os pontos que oferecem aquela vacina específica.
    Caso contrário, retorna todos os relacionamentos entre vacinas e pontos de vacinação.
    """,
    response_description="Lista de vacinas com seus pontos de vacinação",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": [{
                        "vaccine_id": 1,
                        "vaccine_name": "BCG",
                        "vaccination_points": [
                            {
                                "id": 1,
                                "name": "Centro de Vacinação Ponta Verde",
                                "full_address": "Rua Exemplo, 123",
                                "neighborhood": "Ponta Verde",
                                "zip_code": "57000-000",
                                "phone": "(82) 3333-3333",
                                "email": "exemplo@email.com",
                                "latitude": -9.123456,
                                "longitude": -35.123456
                            }
                        ]
                    }]
                }
            }
        }
    }
)
@limiter.limit("10/minute")
async def get_points_by_vaccine(
    request: Request,
    vaccine_id: int | None = Query(None, description="ID da vacina"),
    service: VaccinationPointVaccineService = Depends(get_vaccination_point_vaccine_service)
):
    return await service.get_points_by_vaccine(vaccine_id)

@router.post(
    "/vaccination-points/{vaccination_point_id}/vaccines",
    tags=["Pontos de Vacinação"],
    summary="Adicionar vacina ao ponto",
    description="Adiciona uma vacina a um ponto de vacinação específico",
    response_description="Vacina adicionada com sucesso",
    status_code=201
)
async def add_vaccine_to_point(
    vaccination_point_id: int,
    vaccine: VaccinationPointVaccineCreate,
    service: VaccinationPointVaccineService = Depends(get_vaccination_point_vaccine_service)
):
    return await service.add_vaccine_to_point(vaccination_point_id, vaccine)

@router.delete(
    "/vaccination-points/{vaccination_point_id}/vaccines/{vaccine_id}",
    tags=["Pontos de Vacinação"],
    summary="Remover vacina do ponto",
    description="Remove uma vacina de um ponto de vacinação específico",
    response_description="Vacina removida com sucesso"
)
async def remove_vaccine_from_point(
    vaccination_point_id: int,
    vaccine_id: int,
    service: VaccinationPointVaccineService = Depends(get_vaccination_point_vaccine_service)
):
    return await service.remove_vaccine_from_point(vaccination_point_id, vaccine_id)