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
from sqlalchemy import select, insert
from app.models import VaccinationPointVaccine
from typing import List


class VaccinationPointVaccineRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self, id: int | None = None) -> List[VaccinationPointVaccine]:
        query = select(VaccinationPointVaccine)
        
        if id is not None:
            query = query.where(VaccinationPointVaccine.id == id)
        
        return await self.database.fetch_all(query)

    async def create(
        self, 
        vaccination_point_id: int,
        vaccine_id: int,
    ) -> int:
        query = insert(VaccinationPointVaccine).values(
            vaccination_point_id=vaccination_point_id,
            vaccine_id=vaccine_id,
        )
        return await self.database.execute(query) 