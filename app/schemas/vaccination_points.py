"""
This module contains the Pydantic schemas for the VaccinationPoints resource.
Schemas are responsible for:
- Defining data structure
- Validating input/output data
- Documenting data models
- Converting between different formats

Schemas ensure consistency of data entering and leaving the API.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.common import Schedule


class VaccinationPointCreate(BaseModel):
    city_id: int = Field(
        ...,
        description="City id",
        gt=0
    )
    name: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        description="Vaccination point name"
    )
    schedules: Optional[list[Schedule]] = Field(
        description="""Opening hours of the vaccination point.
        Example: {'start': '00:00:00', 'end': '23:59:59', 'weekday': 'monday'}""",
        default=None,
        validate_default=True,
        json_schema_extra={
            "example": [
                {
                "start": "00:00:00",
                "end": "23:59:59",
                "weekday": "monday"
                }
            ]
        }
    )
    full_address: Optional[str] = Field(
        default=None,
        description="Full address of the vaccination point",
    )
    neighborhood: Optional[str] = Field(
        default=None,
        description="Neighborhood of the vaccination point",
    )
    zip_code: Optional[str] = Field(
        default=None,
        description="Zip code of the vaccination point",
    )
    phone: Optional[str] = Field(
        default=None,
        description="Phone of the vaccination point",
        strict=True
    )
    email: Optional[str] = Field(
        default=None,
        description="Email of the vaccination point",
    )
    website: Optional[str] = Field(
        default=None,
        description="Website of the vaccination point",
    )
    latitude: Optional[float] = Field(
        default=None,
        description="Latitude of the vaccination point",
        strict=True,
        ge=-90,
        le=90
    )
    longitude: Optional[float] = Field(
        default=None,
        description="Longitude of the vaccination point",
        strict=True,
        ge=-180,
        le=180
    )


class VaccinationPointResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    created_at: datetime
    