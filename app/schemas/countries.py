"""
This module contains the Pydantic schemas for the Countries resource.
Schemas are responsible for:
- Defining data structure
- Validating input/output data
- Documenting data models
- Converting between different formats

Schemas ensure consistency of data entering and leaving the API.
"""

from datetime import datetime
from pydantic import BaseModel, Field

    
class CountryCreate(BaseModel):
    name: str = Field(
        ..., 
        min_length=1,
        max_length=255,
        description="Nome do país",
        example="Brasil"
    )
    ibge_code: str | None = Field(
        None, 
        max_length=50,
        description="Código IBGE do país",
        example="1058"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Brasil",
                "ibge_code": "1058"
            }
        }
    
class CountryResponse(BaseModel):
    id: int
    name: str
    ibge_code: str | None
    created_at: datetime
    