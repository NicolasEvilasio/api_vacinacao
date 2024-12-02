"""
Service layer for the VaccinationPointVaccines resource.

This module contains the service layer for managing the relationship
between vaccination points and vaccines.
"""

from fastapi import HTTPException
from app.repositories.vaccination_point_vaccines import VaccinationPointVaccineRepository
from app.repositories.vaccination_points import VaccinationPointRepository
from app.repositories.vaccines import VaccineRepository
from app.schemas.vaccination_point_vaccines import VaccinationPointVaccineCreate
from typing import Dict, List

class VaccinationPointVaccineService:
    def __init__(
        self, 
        repository: VaccinationPointVaccineRepository,
        vaccination_point_repository: VaccinationPointRepository,
        vaccine_repository: VaccineRepository
    ):
        self.repository = repository
        self.vaccination_point_repository = vaccination_point_repository
        self.vaccine_repository = vaccine_repository

    async def get_vaccines_by_point(self, vaccination_point_id: int | None = None) -> List[Dict]:
        # If a point ID was provided, check if it exists
        if vaccination_point_id:
            vaccination_point = await self.vaccination_point_repository.get_by_id(vaccination_point_id)
            if not vaccination_point:
                raise HTTPException(
                    status_code=404,
                    detail=f"Ponto de vacinação com ID {vaccination_point_id} não encontrado"
                )
        
        return await self.repository.get_vaccines_by_point(vaccination_point_id)

    async def get_points_by_vaccine(self, vaccine_id: int | None = None) -> List[Dict]:
        # If a vaccine ID was provided, check if it exists
        if vaccine_id:
            vaccine = await self.vaccine_repository.get_by_id(vaccine_id)
            if not vaccine:
                raise HTTPException(
                    status_code=404,
                    detail=f"Vacina com ID {vaccine_id} não encontrada"
                )
        
        return await self.repository.get_points_by_vaccine(vaccine_id)

    async def add_vaccine_to_point(self, vaccination_point_id: int, data: VaccinationPointVaccineCreate) -> Dict:
        # Check if vaccination point exists
        vaccination_point = await self.vaccination_point_repository.get_by_id(vaccination_point_id)
        if not vaccination_point:
            raise HTTPException(
                status_code=404,
                detail=f"Ponto de vacinação com ID {vaccination_point_id} não encontrado"
            )

        # Check if vaccine exists
        vaccine = await self.vaccine_repository.get_by_id(data.vaccine_id)
        if not vaccine:
            raise HTTPException(
                status_code=404,
                detail=f"Vacina com ID {data.vaccine_id} não encontrada"
            )

        # Check if vaccine is already associated with the point
        existing = await self.repository.get_by_point_and_vaccine(
            vaccination_point_id=vaccination_point_id,
            vaccine_id=data.vaccine_id
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Esta vacina já está cadastrada neste ponto de vacinação"
            )

        last_record_id = await self.repository.create(
            vaccination_point_id=vaccination_point_id,
            vaccine_id=data.vaccine_id
        )
        return {"id": last_record_id, "message": "Vacina adicionada ao ponto com sucesso"}

    async def remove_vaccine_from_point(self, vaccination_point_id: int, vaccine_id: int) -> Dict:
        # Check if vaccination point exists
        vaccination_point = await self.vaccination_point_repository.get_by_id(vaccination_point_id)
        if not vaccination_point:
            raise HTTPException(
                status_code=404,
                detail=f"Ponto de vacinação com ID {vaccination_point_id} não encontrado"
            )

        # Check if vaccine exists
        vaccine = await self.vaccine_repository.get_by_id(vaccine_id)
        if not vaccine:
            raise HTTPException(
                status_code=404,
                detail=f"Vacina com ID {vaccine_id} não encontrada"
            )

        # Check if vaccine is associated with the point
        existing = await self.repository.get_by_point_and_vaccine(
            vaccination_point_id=vaccination_point_id,
            vaccine_id=vaccine_id
        )
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Esta vacina não está cadastrada neste ponto de vacinação"
            )

        success = await self.repository.delete(
            vaccination_point_id=vaccination_point_id,
            vaccine_id=vaccine_id
        )
        return {"message": "Vacina removida do ponto com sucesso"}