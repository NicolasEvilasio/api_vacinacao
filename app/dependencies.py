"""
Application dependencies.

This module contains the injectable dependencies of the application.
Dependencies are responsible for:
- Creating and managing service instances
- Injecting dependencies into controllers
- Configuring the dependency injection system
- Facilitating tests through mocks

This module centralizes the creation of all application dependencies.
"""

from app.database import database
from app.repositories.countries import CountryRepository
from app.repositories.states import StateRepository
from app.repositories.cities import CityRepository
from app.repositories.vaccination_point_vaccines import VaccinationPointVaccineRepository
from app.repositories.vaccination_points import VaccinationPointRepository
from app.repositories.vaccines import VaccineRepository
from app.services.countries import CountryService
from app.services.states import StateService
from app.services.cities import CityService
from app.services.vaccination_points import VaccinationPointService
from app.services.vaccines import VaccineService
from app.services.vaccination_point_vaccines import VaccinationPointVaccineService


def get_country_repository():
    return CountryRepository(database)

def get_country_service():
    repository = get_country_repository()
    return CountryService(repository) 

def get_state_repository():
    return StateRepository(database)

def get_state_service():
    repository = get_state_repository()
    return StateService(repository) 

def get_city_repository():
    return CityRepository(database)

def get_city_service():
    repository = get_city_repository()
    return CityService(repository) 

def get_vaccination_point_repository():
    return VaccinationPointRepository(database)

def get_vaccination_point_service():
    repository = get_vaccination_point_repository()
    return VaccinationPointService(repository) 

def get_vaccine_repository():
    return VaccineRepository(database)

def get_vaccine_service():
    repository = get_vaccine_repository()
    return VaccineService(repository) 

def get_vaccination_point_vaccine_repository():
    return VaccinationPointVaccineRepository(database)

def get_vaccination_point_vaccine_service():
    repository = get_vaccination_point_vaccine_repository()
    return VaccinationPointVaccineService(repository) 
