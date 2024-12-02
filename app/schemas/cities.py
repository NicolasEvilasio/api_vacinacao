"""
This module contains the Pydantic schemas for the Cities resource.
Schemas are responsible for:
- Defining data structure
- Validating input/output data
- Documenting data models
- Converting between different formats

Schemas ensure consistency of data entering and leaving the API.
"""

from datetime import datetime
from pydantic import BaseModel, Field

    
class CityCreate(BaseModel):
    name: str = Field(
        ..., 
        min_length=1,
        max_length=255,
        description="Nome da cidade",
        example="Maceió"
    )
    state_id: int = Field(
        ...,
        description="ID do estado ao qual a cidade pertence",
        gt=0,
        example=1
    )
    ibge_code: str | None = Field(
        None, 
        max_length=50,
        description="Código IBGE da cidade",
        example="2704302"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Maceió",
                "state_id": 1,
                "ibge_code": "2704302"
            }
        }
    
class CityResponse(BaseModel):
    id: int
    name: str
    state_id: int
    ibge_code: str | None
    created_at: datetime
    