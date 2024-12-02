"""
This module contains the repository for the Countries resource.
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
from app.models import Country
from typing import List


class CountryRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self, id: int | None = None, name: str | None = None, ibge_code: str | None = None) -> List[Country]:
        query = select(Country)
        
        if id is not None:
            query = query.where(Country.id == id)
        if name is not None:
            query = query.where(Country.name.ilike(f"%{name}%"))
        if ibge_code is not None:
            query = query.where(Country.ibge_code == ibge_code)
        
        return await self.database.fetch_all(query)

    async def get_by_id(self, id: int) -> Country:
        query = select(Country).where(Country.id == id)
        return await self.database.fetch_one(query) 
    
    async def create(
        self, 
        name: str,
        ibge_code: str | None = None
    ) -> int:
        query = insert(Country).values(
            name=name,
            ibge_code=ibge_code
        )
        return await self.database.execute(query)
