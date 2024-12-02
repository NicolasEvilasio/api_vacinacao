"""
Service layer for the Vaccines resource.

This module contains the service layer for the Vaccines resource.
Services are responsible for:
- Implementing business logic
- Coordinating calls to repositories
- Performing complex validations
- Ensuring data consistency

The service layer should not know details about HTTP or the database,
only business rules.
"""

from app.repositories.vaccines import VaccineRepository
from app.schemas.vaccines import VaccineCreate
from typing import List, Dict

class VaccineService:
    def __init__(self, repository: VaccineRepository):
        self.repository = repository

    async def get_all_vaccines(self, id: int | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id)

    async def create_vaccine(self, vaccine: VaccineCreate) -> Dict:
        last_record_id = await self.repository.create(
            name=vaccine.name
        )
        return {"id": last_record_id, "message": "Vaccine created successfully"} 