"""
Service layer for the Cities resource.

This module contains the service layer for the Cities resource.
Services are responsible for:
- Implementing business logic
- Coordinating calls to repositories
- Performing complex validations
- Ensuring data consistency

The service layer should not know details about HTTP or the database,
only business rules.
"""

from app.repositories.cities import CityRepository
from app.schemas.cities import CityCreate
from typing import List, Dict

class CityService:
    def __init__(self, repository: CityRepository):
        self.repository = repository

    async def get_all_cities(self, id: int | None = None, ibge_code: str | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id, ibge_code=ibge_code)

    async def create_city(self, city: CityCreate) -> Dict:
        last_record_id = await self.repository.create(
            state_id=city.state_id,
            name=city.name,
            ibge_code=city.ibge_code
        )
        return {"id": last_record_id, "message": "City created successfully"} 