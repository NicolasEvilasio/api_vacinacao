"""
Service layer for the States resource.

This module contains the service layer for the States resource.
Services are responsible for:
- Implementing business logic
- Coordinating calls to repositories
- Performing complex validations
- Ensuring data consistency

The service layer should not know details about HTTP or the database,
only business rules.
"""

from fastapi import HTTPException
from app.repositories.states import StateRepository
from app.repositories.countries import CountryRepository
from app.schemas.states import StateCreate
from typing import Dict, List

class StateService:
    def __init__(self, repository: StateRepository):
        self.repository = repository
        self.country_repository = CountryRepository(self.repository.database)

    async def get_all_states(self, id: int | None = None, ibge_code: str | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id, ibge_code=ibge_code)

    async def create_state(self, state: StateCreate) -> Dict:
        # Verifica se o país existe
        country = await self.country_repository.get_by_id(state.country_id)
        if not country:
            raise HTTPException(
                status_code=404,
                detail=f"País com ID {state.country_id} não encontrado"
            )
            
        last_record_id = await self.repository.create(
            country_id=state.country_id,
            name=state.name,
            ibge_code=state.ibge_code
        )
        return {"id": last_record_id, "message": "State created successfully"} 