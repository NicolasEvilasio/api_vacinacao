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
from fastapi import HTTPException

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

    async def get_vaccines_by_point(self, vaccination_point_id: int | None = None) -> List[Dict]:
        results = await self.repository.get_vaccines_by_point(vaccination_point_id)
        
        # Organizar os resultados por ponto de vacinação
        organized_results = {}
        for result in results:
            point_id = result['vaccination_point_id']
            if point_id not in organized_results:
                organized_results[point_id] = {
                    'vaccination_point_id': point_id,
                    'vaccination_point_name': result['vaccination_point_name'],
                    'vaccines': []
                }
            organized_results[point_id]['vaccines'].append({
                'id': result['vaccine_id'],
                'name': result['vaccine_name']
            })
        
        return list(organized_results.values())

    async def get_points_by_vaccine(self, vaccine_id: int | None = None) -> List[Dict]:
        results = await self.repository.get_points_by_vaccine(vaccine_id)
        
        # Organizar os resultados por vacina
        organized_results = {}
        for result in results:
            vaccine_id = result['vaccine_id']
            if vaccine_id not in organized_results:
                organized_results[vaccine_id] = {
                    'vaccine_id': vaccine_id,
                    'vaccine_name': result['vaccine_name'],
                    'vaccination_points': []
                }
            organized_results[vaccine_id]['vaccination_points'].append({
                'id': result['vaccination_point_id'],
                'name': result['vaccination_point_name'],
                'full_address': result['full_address'],
                'neighborhood': result['neighborhood'],
                'zip_code': result['zip_code'],
                'phone': result['phone'],
                'email': result['email'],
                'latitude': result['latitude'],
                'longitude': result['longitude']
            })
        
        return list(organized_results.values())

    async def add_vaccine_to_point(self, vaccination_point_id: int, data: VaccinationPointVaccineCreate) -> Dict:
        # Aqui você pode adicionar validações adicionais se necessário
        last_record_id = await self.repository.create(
            vaccination_point_id=vaccination_point_id,
            vaccine_id=data.vaccine_id
        )
        return {"id": last_record_id, "message": "Vacina adicionada ao ponto com sucesso"}

    async def remove_vaccine_from_point(
        self,
        vaccination_point_id: int,
        vaccine_id: int
    ) -> Dict:
        success = await self.repository.delete(
            vaccination_point_id=vaccination_point_id,
            vaccine_id=vaccine_id
        )
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Relacionamento entre ponto de vacinação e vacina não encontrado"
            )
        return {"message": "Vacina removida do ponto com sucesso"}