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
from app.schemas.states import StateCreate, StateUpdate
from typing import Dict, List
from sqlalchemy.exc import IntegrityError

class StateService:
    def __init__(self, repository: StateRepository):
        self.repository = repository
        self.country_repository = CountryRepository(self.repository.database)

    async def get_all_states(self, id: int | None = None, name: str | None = None, ibge_code: str | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id, name=name, ibge_code=ibge_code)

    async def create_state(self, state: StateCreate) -> Dict:
        # Verifica se o país existe
        country = await self.country_repository.get_by_id(state.country_id)
        if not country:
            raise HTTPException(
                status_code=404,
                detail=f"País com ID {state.country_id} não encontrado"
            )
        
        # Verifica se já existe um estado com o mesmo código IBGE
        existing_state = await self.repository.get_by_ibge_code(state.ibge_code)
        if existing_state:
            raise HTTPException(
                status_code=400,
                detail="Código IBGE já cadastrado para outro estado."
            )
        
        try:
            last_record_id = await self.repository.create(
                country_id=state.country_id,
                name=state.name,
                ibge_code=state.ibge_code
            )
            return {"id": last_record_id, "message": "Estado criado com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar o estado."
            )

    async def update_state(self, id: int, state: StateUpdate) -> Dict:
        existing = await self.repository.get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"Estado com ID {id} não encontrado"
            )
        
        # Verifica se já existe um estado com o mesmo código IBGE
        if state.ibge_code:
            existing_state = await self.repository.get_by_ibge_code(state.ibge_code)
            if existing_state and existing_state.id != id:
                raise HTTPException(
                    status_code=400,
                    detail="Código IBGE já cadastrado para outro estado."
                )
        
        update_data = state.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Nenhum dado fornecido para atualização"
            )
        
        try:
            success = await self.repository.update(id, update_data)
            return {"message": "Estado atualizado com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Erro ao atualizar o estado."
            )

    async def delete_state(self, id: int) -> Dict:
        existing = await self.repository.get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"Estado com ID {id} não encontrado"
            )
        
        success = await self.repository.delete(id)
        return {"message": "Estado excluído com sucesso"}