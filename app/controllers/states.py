"""
This module contains the controllers (route handlers) for the States resource.
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
from app.schemas.states import StateCreate
from app.services.states import StateService
from app.dependencies import get_state_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/states",
    tags=["Estados"],
    summary="Listar estados",
    description="Retorna todos os estados cadastrados"
)
@limiter.limit("10/minute")
async def get_states(
    request: Request,
    id: int | None = None,
    ibge_code: str | None = None,
    service: StateService = Depends(get_state_service)
):
    return await service.get_all_states(id=id, ibge_code=ibge_code)

@router.post(
    "/states",
    tags=["Estados"],
    summary="Cadastrar um estado",
    description="Cadastra um estado"
)
async def create_state(
    state: StateCreate,
    service: StateService = Depends(get_state_service)
):
    return await service.create_state(state)