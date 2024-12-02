"""
This module contains the repository for the Cities resource.
Repositories are responsible for:
- Performing database operations
- Implementing SQL queries
- Mapping database results to models
- Managing transactions

The repository should not contain business logic, only data
access operations.
"""

from databases import Database
from sqlalchemy import select, insert
from app.models import City
from typing import List


class CityRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self, id: int | None = None, name: str | None = None, ibge_code: str | None = None) -> List[City]:
        query = select(City)
        
        if id is not None:
            query = query.where(City.id == id)
        if name is not None:
            query = query.where(City.name.ilike(f"%{name}%"))
        if ibge_code is not None:
            query = query.where(City.ibge_code == ibge_code)
            
        return await self.database.fetch_all(query)

    async def create(
        self,
        state_id: int,
        name: str,
        ibge_code: str | None = None,
    ) -> int:
        query = insert(City).values(
            state_id=state_id,
            name=name,
            ibge_code=ibge_code,
        )
        return await self.database.execute(query) 