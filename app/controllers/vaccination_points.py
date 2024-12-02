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

from fastapi import APIRouter, Depends, Request, Form
from typing import Annotated
from app.schemas.vaccination_points import VaccinationPointCreate
from app.services.vaccination_points import VaccinationPointService
from app.dependencies import get_vaccination_point_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/vaccination-points",
    tags=["Pontos de Vacinação"],
    summary="Listar pontos de vacinação",
    description="Retorna todos os pontos de vacinação cadastrados"
)
@limiter.limit("10/minute")
async def get_vaccination_points(
    request: Request,
    city_id: int | None = None,
    service: VaccinationPointService = Depends(get_vaccination_point_service)
):
    return await service.get_all_vaccination_points(city_id=city_id)

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