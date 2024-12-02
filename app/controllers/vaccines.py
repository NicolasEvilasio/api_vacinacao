"""
This module contains the controllers (route handlers) for the Vaccines resource.
The controllers are responsible for:
- Receiving HTTP requests
- Validating input data
- Calling appropriate services
- Returning formatted HTTP responses

Controllers should not contain business logic, only HTTP request 
handling logic.
"""

from fastapi import APIRouter, Depends, Request, Query
from app.schemas.vaccines import VaccineCreate
from app.services.vaccines import VaccineService
from app.dependencies import get_vaccine_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/vaccines",
    tags=["Vacinas"],
    summary="Listar vacinas",
    description="""
    Retorna a lista de vacinas cadastradas.
    
    Filtros disponíveis:
    * ID da vacina
    * Nome da vacina (busca parcial, não sensível a maiúsculas/minúsculas)
    
    Se nenhum filtro for fornecido, retorna todas as vacinas.
    """,
    response_description="Lista de vacinas",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "BCG",
                        "created_at": "2024-01-01T00:00:00"
                    }]
                }
            }
        }
    }
)
@limiter.limit("10/minute")
async def get_vaccines(
    request: Request,
    id: int | None = Query(None, description="ID da vacina"),
    name: str | None = Query(None, description="Nome da vacina (busca parcial)"),
    service: VaccineService = Depends(get_vaccine_service)
):
    return await service.get_all_vaccines(id=id, name=name)

@router.post(
    "/vaccines",
    tags=["Vacinas"],
    summary="Cadastrar uma vacina",
    description="Cadastra uma nova vacina no sistema",
    response_description="Vacina criada com sucesso",
    status_code=201,
    responses={
        201: {
            "description": "Vacina criada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "message": "Vacina criada com sucesso"
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
                                "msg": "O nome da vacina é obrigatório",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def create_vaccine(
    vaccine: VaccineCreate,
    service: VaccineService = Depends(get_vaccine_service)
):
    return await service.create_vaccine(vaccine) 