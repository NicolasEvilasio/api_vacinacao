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

from fastapi import APIRouter, Depends, Request, Query
from app.models import State
from app.schemas.states import StateCreate, StateUpdate
from app.services.states import StateService
from app.dependencies import get_state_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/states",
    tags=["Estados"],
    summary="Listar estados",
    description="""Retorna a lista de estados cadastrados.""",
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
    description="Cadastra um novo estado no sistema",
    response_description="Estado criado com sucesso",
    status_code=201
)
async def create_state(
    state: StateCreate,
    service: StateService = Depends(get_state_service)
):
    return await service.create_state(state)

@router.patch(
    "/states/{id}",
    tags=["Estados"],
    summary="Atualizar um estado",
    description="Atualiza parcialmente os dados de um estado específico",
    response_description="Estado atualizado com sucesso",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Estado atualizado com sucesso"
                    }
                }
            }
        },
        404: {
            "description": "Estado não encontrado"
        }
    }
)
async def update_state(
    id: int,
    state: StateUpdate,
    service: StateService = Depends(get_state_service)
):
    return await service.update_state(id, state)

@router.delete(
    "/states/{id}",
    tags=["Estados"],
    summary="Excluir um estado",
    description="Remove um estado do sistema",
    response_description="Estado excluído com sucesso",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Estado excluído com sucesso"
                    }
                }
            }
        },
        404: {
            "description": "Estado não encontrado"
        }
    }
)
async def delete_state(
    id: int,
    service: StateService = Depends(get_state_service)
):
    return await service.delete_state(id)