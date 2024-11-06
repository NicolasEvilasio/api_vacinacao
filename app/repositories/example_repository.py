"""
Repositório para exemplos.

Este módulo contém o repositório para o recurso Example.
Os repositórios são responsáveis por:
- Realizar operações no banco de dados
- Implementar queries SQL
- Mapear resultados do banco para modelos
- Gerenciar transações

O repositório não deve conter lógica de negócio, apenas operações
de acesso a dados.
"""

from databases import Database
from sqlalchemy import select, insert
from app.models import Example
from typing import List, Optional

class ExampleRepository:
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self) -> List[Example]:
        query = select(Example)
        return await self.database.fetch_all(query)

    async def create(self, name: str, description: Optional[str]) -> int:
        query = insert(Example).values(
            name=name,
            description=description
        )
        return await self.database.execute(query) 