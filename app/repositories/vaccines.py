"""
This module contains the repository for the Vaccines resource.
Repositories are responsible for:
- Performing database operations
- Implementing SQL queries
- Mapping database results to models
- Managing transactions

The repository should not contain business logic, only data
access operations.
"""

from databases import Database
from sqlalchemy import select, insert, update, delete
from app.models import Vaccine
from typing import List


class VaccineRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self, id: int | None = None, name: str | None = None) -> List[Vaccine]:
        query = select(Vaccine)
        
        if id is not None:
            query = query.where(Vaccine.id == id)
        if name is not None:
            query = query.where(Vaccine.name.ilike(f"%{name}%"))
        
        return await self.database.fetch_all(query)

    async def get_by_id(self, id: int) -> Vaccine:
        query = select(Vaccine).where(Vaccine.id == id)
        return await self.database.fetch_one(query)

    async def create(
        self, 
        name: str
    ) -> int:
        query = insert(Vaccine).values(
            name=name
        )
        return await self.database.execute(query)

    async def update(
        self,
        id: int,
        data: dict
    ) -> bool:
        query = update(Vaccine).where(
            Vaccine.id == id
        ).values(**data)
        result = await self.database.execute(query)
        return result > 0

    async def delete(
        self,
        id: int
    ) -> bool:
        query = delete(Vaccine).where(
            Vaccine.id == id
        )
        result = await self.database.execute(query)
        return result > 0 