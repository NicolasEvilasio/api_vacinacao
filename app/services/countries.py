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
from app.schemas.countries import CountryCreate, CountryUpdate
from typing import List, Dict
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class CountryService:
    def __init__(self, repository: CountryRepository):
        self.repository = repository

    async def get_all_countries(self, id: int | None = None, name: str | None = None, ibge_code: str | None = None) -> List[Dict]:
        return await self.repository.get_all(id=id, name=name, ibge_code=ibge_code)

    async def create_country(self, country: CountryCreate) -> Dict:
        # Verifica se já existe um país com o mesmo código IBGE
        existing_country = await self.repository.get_by_ibge_code(country.ibge_code)
        if existing_country:
            raise HTTPException(
                status_code=400,
                detail="Código IBGE já cadastrado para outro país."
            )

        try:
            last_record_id = await self.repository.create(
                name=country.name,
                ibge_code=country.ibge_code
            )
            return {"id": last_record_id, "message": "País criado com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar o país."
            )

    async def update_country(self, id: int, country: CountryUpdate) -> Dict:
        existing = await self.repository.get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"País com ID {id} não encontrado"
            )
        
        # Verifica se já existe um país com o mesmo código IBGE
        if country.ibge_code:
            existing_country = await self.repository.get_by_ibge_code(country.ibge_code)
            if existing_country and existing_country.id != id:
                raise HTTPException(
                    status_code=400,
                    detail="Código IBGE já cadastrado para outro país."
                )
        
        update_data = country.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Nenhum dado fornecido para atualização"
            )
        
        try:
            success = await self.repository.update(id, update_data)
            return {"message": "País atualizado com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Erro ao atualizar o país."
            )

    async def delete_country(self, id: int) -> Dict:
        existing = await self.repository.get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"País com ID {id} não encontrado"
            )
        
        success = await self.repository.delete(id)
        return {"message": "País excluído com sucesso"} 