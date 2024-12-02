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
    vaccine_id: int = Field(
        ...,
        description="ID da vacina",
        gt=0,
        example=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "vaccine_id": 1
            }
        }

class VaccinationPointVaccineResponse(BaseModel):
    id: int 
    vaccination_point_id: int
    vaccine_id: int
    created_at: datetime
    