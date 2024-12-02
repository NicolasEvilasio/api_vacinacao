"""
Service layer for the Countries resource.

This module contains the service layer for the Countries resource.
Services are responsible for:
- Implementing business logic
- Coordinating calls to repositories
- Performing complex validations
- Ensuring data consistency

The service layer should not know details about HTTP or the database,
only business rules.
"""

from app.repositories.countries import CountryRepository
from app.schemas.countries import CountryCreate
from typing import List, Dict

class CountryService:
    def __init__(self, repository: CountryRepository):
        self.repository = repository

    async def get_all_countries(self, id: int | None = None, name: str | None = None, ibge_code: str | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id, name=name, ibge_code=ibge_code)

    async def create_country(self, country: CountryCreate) -> Dict:
        last_record_id = await self.repository.create(
            name=country.name,
            ibge_code=country.ibge_code
        )
        return {"id": last_record_id, "message": "Country created successfully"} 