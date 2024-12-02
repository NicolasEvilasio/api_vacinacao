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

from fastapi import APIRouter, Depends, Request, Form, Query
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
    description="""
    Retorna a lista de estados cadastrados.
    
    Filtros disponíveis:
    * ID do estado
    * Nome do estado (busca parcial, não sensível a maiúsculas/minúsculas)
    * Código IBGE
    
    Se nenhum filtro for fornecido, retorna todos os estados.
    """,
    response_description="Lista de estados"
)
@limiter.limit("10/minute")
async def get_states(
    request: Request,
    id: int | None = Query(None, description="ID do estado"),
    name: str | None = Query(None, description="Nome do estado (busca parcial)"),
    ibge_code: str | None = Query(None, description="Código IBGE do estado"),
    service: StateService = Depends(get_state_service)
):
    return await service.get_all_states(id=id, name=name, ibge_code=ibge_code)

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