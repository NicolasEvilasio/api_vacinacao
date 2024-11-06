"""
Schemas para exemplos.

Este módulo contém os schemas Pydantic para o recurso Example.
Os schemas são responsáveis por:
- Definir a estrutura dos dados
- Validar dados de entrada/saída
- Documentar os modelos de dados
- Converter entre diferentes formatos

Os schemas garantem a consistência dos dados que entram e saem da API.
"""

from pydantic import BaseModel, Field
from typing import Optional

class ExampleCreate(BaseModel):
    name: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9 ]*$",
        description="Nome do exemplo"
    )
    description: Optional[str] = Field(
        None, 
        description="Descrição detalhada do exemplo"
    )

class ExampleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] 