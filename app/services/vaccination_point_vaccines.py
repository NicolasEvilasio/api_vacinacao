"""
Service layer for the VaccinationPointVaccines resource.

This module contains the service layer for the VaccinationPointVaccines resource.
Services are responsible for:
- Implementing business logic
- Coordinating calls to repositories
- Performing complex validations
- Ensuring data consistency

The service layer should not know details about HTTP or the database,
only business rules.
"""

from app.repositories.vaccination_point_vaccines import VaccinationPointVaccineRepository
from app.schemas.vaccination_point_vaccines import VaccinationPointVaccineCreate
from typing import List, Dict

class VaccinationPointVaccineService:
    def __init__(self, repository: VaccinationPointVaccineRepository):
        self.repository = repository

    async def get_all_vaccines(self) -> List[Dict]:
        return await self.repository.get_all()

    async def create_vaccination_point_vaccine(self, vaccination_point_vaccine: VaccinationPointVaccineCreate) -> Dict:
        last_record_id = await self.repository.create(
            vaccination_point_id=vaccination_point_vaccine.vaccination_point_id,
            vaccine_id=vaccination_point_vaccine.vaccine_id
        )
        return {"id": last_record_id, "message": "Vaccination point vaccine created successfully"}

    async def get_all_vaccination_point_vaccines(self, id: int | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id)