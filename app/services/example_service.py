"""
Serviço para exemplos.

Este módulo contém a camada de serviço para o recurso Example.
Os serviços são responsáveis por:
- Implementar a lógica de negócio
- Coordenar chamadas aos repositórios
- Realizar validações complexas
- Garantir a consistência dos dados

A camada de serviço não deve conhecer detalhes HTTP ou do banco de dados,
apenas regras de negócio.
"""

from app.repositories.example_repository import ExampleRepository
from app.schemas.example import ExampleCreate
from typing import List, Dict

class ExampleService:
    def __init__(self, repository: ExampleRepository):
        self.repository = repository

    async def get_all_examples(self) -> List[Dict]:
        return await self.repository.get_all()

    async def create_example(self, example: ExampleCreate) -> Dict:
        last_record_id = await self.repository.create(
            name=example.name,
            description=example.description
        )
        return {"id": last_record_id, "message": "Registro criado com sucesso"} 