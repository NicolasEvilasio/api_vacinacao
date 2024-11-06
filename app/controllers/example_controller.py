"""
Controller para exemplos.

Este módulo contém os controllers (manipuladores de rotas) para o recurso Example.
Os controllers são responsáveis por:
- Receber requisições HTTP
- Validar dados de entrada
- Chamar os serviços apropriados
- Retornar respostas HTTP formatadas

Os controllers não devem conter lógica de negócio, apenas a lógica de 
manipulação de requisições HTTP.
"""

from fastapi import APIRouter, Depends, Request
from app.schemas.example import ExampleCreate
from app.services.example_service import ExampleService
from app.dependencies import get_example_service
from app.config import limiter

router = APIRouter()

@router.get(
    "/examples",
    tags=["Examples"],
    summary="Listar exemplos",
    description="Retorna todos os exemplos cadastrados"
)
@limiter.limit("10/minute")
async def get_examples(
    request: Request,
    service: ExampleService = Depends(get_example_service)
):
    return await service.get_all_examples()

@router.post(
    "/examples/",
    tags=["Examples"],
    summary="Criar exemplo",
    description="Cria um novo exemplo"
)
async def create_example(
    example: ExampleCreate,
    service: ExampleService = Depends(get_example_service)
):
    return await service.create_example(example) 