"""
Service layer for the VaccinationPoints resource.

This module contains the service layer for the VaccinationPoints resource.
Services are responsible for:
- Implementing business logic
- Coordinating calls to repositories
- Performing complex validations
- Ensuring data consistency

The service layer should not know details about HTTP or the database,
only business rules.
"""

from app.repositories.vaccination_points import VaccinationPointRepository
from app.schemas.vaccination_points import VaccinationPointCreate
from typing import List, Dict

class VaccinationPointService:
    def __init__(self, repository: VaccinationPointRepository):
        self.repository = repository

    async def get_all_vaccination_points(self, id: int | None = None, name: str | None = None, city_id: int | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id, name=name, city_id=city_id)

    async def create_vaccination_point(self, vaccination_point: VaccinationPointCreate) -> Dict:
        last_record_id = await self.repository.create(
            name=vaccination_point.name,
            city_id=vaccination_point.city_id
        )
        return {"id": last_record_id, "message": "Vaccination point created successfully"} 