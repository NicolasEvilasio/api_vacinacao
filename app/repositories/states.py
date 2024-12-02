"""
This module contains the repository for the States resource.
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
from app.models import State
from typing import List


class StateRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self, id: int | None = None, ibge_code: str | None = None) -> List[State]:
        query = select(State)
        
        if id is not None:
            query = query.where(State.id == id)
        if ibge_code is not None:
            query = query.where(State.ibge_code == ibge_code)
            
        return await self.database.fetch_all(query)

    async def create(
        self,
        country_id: int,
        name: str,
        ibge_code: str | None = None,
    ) -> int:
        query = insert(State).values(
            country_id=country_id,
            name=name,
            ibge_code=ibge_code,
        )
        return await self.database.execute(query) 