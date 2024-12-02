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
from sqlalchemy import select, insert, join
from app.models import VaccinationPointVaccine, Vaccine, VaccinationPoint
from typing import List, Dict


class VaccinationPointVaccineRepository:   
    def __init__(self, database: Database):
        self.database = database

    async def get_vaccines_by_point(self, vaccination_point_id: int | None = None) -> List[Dict]:
        # Join com a tabela de vacinas
        query = select(
            VaccinationPointVaccine.vaccination_point_id,
            VaccinationPoint.name.label('vaccination_point_name'),
            Vaccine.id.label('vaccine_id'),
            Vaccine.name.label('vaccine_name')
        ).join(
            Vaccine,
            VaccinationPointVaccine.vaccine_id == Vaccine.id
        ).join(
            VaccinationPoint,
            VaccinationPointVaccine.vaccination_point_id == VaccinationPoint.id
        )
        
        if vaccination_point_id is not None:
            query = query.where(VaccinationPointVaccine.vaccination_point_id == vaccination_point_id)
            
        return await self.database.fetch_all(query)

    async def get_points_by_vaccine(self, vaccine_id: int | None = None) -> List[Dict]:
        # Join com a tabela de pontos de vacinação
        query = select(
            VaccinationPointVaccine.vaccine_id,
            Vaccine.name.label('vaccine_name'),
            VaccinationPoint.id.label('vaccination_point_id'),
            VaccinationPoint.name.label('vaccination_point_name'),
            VaccinationPoint.full_address,
            VaccinationPoint.neighborhood,
            VaccinationPoint.zip_code,
            VaccinationPoint.phone,
            VaccinationPoint.email,
            VaccinationPoint.latitude,
            VaccinationPoint.longitude
        ).join(
            VaccinationPoint,
            VaccinationPointVaccine.vaccination_point_id == VaccinationPoint.id
        ).join(
            Vaccine,
            VaccinationPointVaccine.vaccine_id == Vaccine.id
        )
        
        if vaccine_id is not None:
            query = query.where(VaccinationPointVaccine.vaccine_id == vaccine_id)
            
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