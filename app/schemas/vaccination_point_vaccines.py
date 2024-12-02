"""
This module contains the Pydantic schemas for the VaccinationPointVaccines resource.
Schemas are responsible for:
- Defining data structure
- Validating input/output data
- Documenting data models
- Converting between different formats

Schemas ensure consistency of data entering and leaving the API.
"""

from datetime import datetime
from pydantic import BaseModel, Field

    
class VaccinationPointVaccineCreate(BaseModel):
    vaccination_point_id: int = Field(
        ..., 
        description="Vaccination point id",
        gt=0
    )
    vaccine_id: int = Field(
        ..., 
        description="Vaccine id",
        gt=0
    )

    
class VaccinationPointVaccineResponse(BaseModel):
    id: int 
    vaccination_point_id: int
    vaccine_id: int
    created_at: datetime
    