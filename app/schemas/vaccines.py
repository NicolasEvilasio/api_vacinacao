"""
This module contains the Pydantic schemas for the Vaccines resource.
Schemas are responsible for:
- Defining data structure
- Validating input/output data
- Documenting data models
- Converting between different formats

Schemas ensure consistency of data entering and leaving the API.
"""

from datetime import datetime
from pydantic import BaseModel, Field

    
class VaccineCreate(BaseModel):
    name: str = Field(
        ..., 
        min_length=1,
        max_length=255,
        description="Nome da vacina",
        example="BCG"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "BCG"
            }
        }
    
class VaccineResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    