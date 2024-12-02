"""
This module contains the Pydantic schemas for the States resource.
Schemas are responsible for:
- Defining data structure
- Validating input/output data
- Documenting data models
- Converting between different formats

Schemas ensure consistency of data entering and leaving the API.
"""

from datetime import datetime
from pydantic import BaseModel, Field

    
class StateCreate(BaseModel):
    name: str = Field(
        ..., 
        min_length=1,
        max_length=255,
        description="Nome do estado",
        example="Alagoas"
    )
    country_id: int = Field(
        ...,
        description="ID do país ao qual o estado pertence",
        gt=0,
        example=1
    )
    ibge_code: str | None = Field(
        None, 
        max_length=50,
        description="Código IBGE do estado",
        example="27"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alagoas",
                "country_id": 1,
                "ibge_code": "27"
            }
        }
    
class StateResponse(BaseModel):
    id: int
    name: str
    country_id: int
    ibge_code: str | None
    created_at: datetime
    
class StateUpdate(BaseModel):
    name: str | None = Field(
        None, 
        min_length=1,
        max_length=255,
        description="Nome do estado",
        example="Alagoas"
    )
    country_id: int | None = Field(
        None,
        description="ID do país ao qual o estado pertence",
        gt=0,
        example=1
    )
    ibge_code: str | None = Field(
        None, 
        max_length=50,
        description="Código IBGE do estado",
        example="27"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alagoas",
                "country_id": 1,
                "ibge_code": "27"
            }
        }
    