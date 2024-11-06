"""
Dependências da aplicação.

Este módulo contém as dependências injetáveis da aplicação.
As dependências são responsáveis por:
- Criar e gerenciar instâncias de serviços
- Injetar dependências nos controllers
- Configurar o sistema de injeção de dependências
- Facilitar testes através de mocks

Este módulo centraliza a criação de todas as dependências da aplicação.
"""

from app.database import database
from app.repositories.example_repository import ExampleRepository
from app.services.example_service import ExampleService

def get_example_repository():
    return ExampleRepository(database)

def get_example_service():
    repository = get_example_repository()
    return ExampleService(repository) 