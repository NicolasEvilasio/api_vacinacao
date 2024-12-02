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
from app.schemas.cities import CityCreate, CityUpdate
from typing import List, Dict
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class CityService:
    def __init__(self, repository: CityRepository):
        self.repository = repository

    async def get_all_cities(self, id: int | None = None, name: str | None = None, ibge_code: str | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id, name=name, ibge_code=ibge_code)

    async def create_city(self, city: CityCreate) -> Dict:
        # Verifica se já existe uma cidade com o mesmo código IBGE
        existing_city = await self.repository.get_by_ibge_code(city.ibge_code)
        if existing_city:
            raise HTTPException(
                status_code=400,
                detail="Código IBGE já cadastrado para outra cidade."
            )

        try:
            last_record_id = await self.repository.create(
                state_id=city.state_id,
                name=city.name,
                ibge_code=city.ibge_code
            )
            return {"id": last_record_id, "message": "Cidade criada com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar a cidade."
            )

    async def update_city(self, id: int, city: CityUpdate) -> Dict:
        existing = await self.repository.get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"Cidade com ID {id} não encontrada"
            )
        
        update_data = city.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Nenhum dado fornecido para atualização"
            )
        
        try:
            success = await self.repository.update(id, update_data)
            return {"message": "Cidade atualizada com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Código IBGE já cadastrado para outra cidade."
            )

    async def delete_city(self, id: int) -> Dict:
        existing = await self.repository.get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"Cidade com ID {id} não encontrada"
            )
        
        success = await self.repository.delete(id)
        return {"message": "Cidade excluída com sucesso"}