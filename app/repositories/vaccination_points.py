"""
This module contains the repository for the VaccinationPoints resource.
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
from app.models import VaccinationPoint
from typing import List, Optional
from app.schemas.common import Schedule

class VaccinationPointRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self, id: int | None = None, name: str | None = None, city_id: int | None = None) -> List[VaccinationPoint]:
        query = select(VaccinationPoint)
        
        if id is not None:
            query = query.where(VaccinationPoint.id == id)
        if name is not None:
            query = query.where(VaccinationPoint.name.ilike(f"%{name}%"))
        if city_id is not None:
            query = query.where(VaccinationPoint.city_id == city_id)
            
        return await self.database.fetch_all(query)

    async def get_by_id(self, id: int) -> VaccinationPoint:
        query = select(VaccinationPoint).where(VaccinationPoint.id == id)
        return await self.database.fetch_one(query)

    async def create(
        self, 
        city_id: int,
        name: str,
        schedules: Optional[list[Schedule]] = None,
        full_address: str | None = None,
        neighborhood: str | None = None,
        zip_code: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        website: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None
    ) -> int:
        # Converte a lista de Schedule para formato JSON
        schedules_list = [schedule.model_dump() for schedule in schedules] if schedules else None
        
        query = insert(VaccinationPoint).values(
            city_id=city_id,
            name=name,
            schedules=schedules_list,
            full_address=full_address,
            neighborhood=neighborhood,
            zip_code=zip_code,
            phone=phone,
            email=email,
            website=website,
            latitude=latitude,
            longitude=longitude
        )
        return await self.database.execute(query)

    async def update(
        self,
        id: int,
        data: dict
    ) -> bool:
        query = update(VaccinationPoint).where(
            VaccinationPoint.id == id
        ).values(**data)
        result = await self.database.execute(query)
        return result > 0

    async def delete(
        self,
        id: int
    ) -> bool:
        query = delete(VaccinationPoint).where(
            VaccinationPoint.id == id
        )
        result = await self.database.execute(query)
        return result > 0 