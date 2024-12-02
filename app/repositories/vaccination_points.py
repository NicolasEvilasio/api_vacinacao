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
from sqlalchemy import JSON, select, insert
from app.models import VaccinationPoint
from typing import List, Optional

from app.schemas.common import Schedule

class VaccinationPointRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self, city_id: int | None = None) -> List[VaccinationPoint]:
        query = select(VaccinationPoint)
        
        if city_id is not None:
            query = query.where(VaccinationPoint.city_id == city_id)
            
        return await self.database.fetch_all(query)

    async def create(
        self, 
        city_id: int,
        name: str,
        schedules: Optional[list[Schedule]] = None,
        full_address: Optional[str] = None,
        neighborhood: Optional[str] = None,
        zip_code: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> int:
        schedules_list = [schedule.model_dump() for schedule in schedules] if schedules else None
                
        query = insert(VaccinationPoint).values(
            city_id=city_id,
            name=name,
            schedules = schedules_list,
            full_address = full_address,
            neighborhood = neighborhood,
            zip_code = zip_code,
            phone = phone,
            email = email,
            website = website,
            latitude = latitude,
            longitude = longitude
        )
        return await self.database.execute(query) 