from pathlib import Path
from sqlalchemy import create_engine
from app.models import Base
from app.database import DATABASE_URL
from app.repositories.countries import CountryRepository
from app.repositories.states import StateRepository
from app.repositories.cities import CityRepository
from app.repositories.vaccination_points import VaccinationPointRepository
from app.repositories.vaccines import VaccineRepository
from app.repositories.vaccination_point_vaccines import VaccinationPointVaccineRepository
from app.database import database
from app.schemas.common import Schedule
from app.schemas.countries import CountryCreate
from app.schemas.states import StateCreate
from app.schemas.cities import CityCreate
from app.schemas.vaccination_points import VaccinationPointCreate
from app.schemas.vaccines import VaccineCreate
from app.schemas.vaccination_point_vaccines import VaccinationPointVaccineCreate
from app.config import logger, settings
import json
import asyncio
import os

# Get the absolute path to the current module's directory
BASE_DIR = Path(__file__).parents[1]

def init_database():
    # Ensures that the data directory exists if using SQLite
    if settings.DATABASE_TYPE == "sqlite":
        logger.info("Creating data directory...")
        os.makedirs("data", exist_ok=True)
        
    engine = create_engine(DATABASE_URL)
    logger.info("Creating tables...")
    Base.metadata.create_all(engine)
    logger.info("All tables created successfully!")

async def load_json_data():
    await database.connect()
    
    try:
        # Load and create countries
        logger.info("Creating countries...")
        with open(BASE_DIR / 'data' / 'countries.json', 'r', encoding='utf-8') as file:
            countries_data = json.load(file)
        country_repository = CountryRepository(database)
        for country in countries_data:
            await country_repository.create(
                name=country['name'],
                ibge_code=country.get('ibge_code')
            )
        
        # Load and create states
        logger.info("Creating states...")
        with open(BASE_DIR / 'data' / 'states.json', 'r', encoding='utf-8') as file:
            states_data = json.load(file)
        state_repository = StateRepository(database)
        for state in states_data:
            await state_repository.create(
                name=state['name'],
                country_id=state['country_id'],
                ibge_code=state.get('ibge_code')
            )
        
        # Load and create cities
        logger.info("Creating cities...")
        with open(BASE_DIR / 'data' / 'cities.json', 'r', encoding='utf-8') as file:
            cities_data = json.load(file)
        city_repository = CityRepository(database)
        for city in cities_data:
            await city_repository.create(
                name=city['name'],
                state_id=city['state_id'],
                ibge_code=city.get('ibge_code')
            )
        
        # Load and create vaccination points
        logger.info("Creating vaccination points...")
        with open(BASE_DIR / 'data' / 'vaccination_points.json', 'r', encoding='utf-8') as file:
            vaccination_points_data = json.load(file)
        vaccination_point_repository = VaccinationPointRepository(database)
        for point in vaccination_points_data:
            await vaccination_point_repository.create(
                city_id=point['city_id'],
                name=point['name'],
                schedules=[Schedule(**schedule) for schedule in point['schedules']],
                full_address=point['full_address'],
                neighborhood=point['neighborhood'],
                zip_code=point['zip_code'],
                phone=point['phone'],
                email=point['email'],
                website=point['website'],
                latitude=point['latitude'],
                longitude=point['longitude']
            )
        
        # Load and create vaccines
        logger.info("Creating vaccines...")
        with open(BASE_DIR / 'data' / 'vaccines.json', 'r', encoding='utf-8') as file:
            vaccines_data = json.load(file)
        vaccine_repository = VaccineRepository(database)
        for vaccine in vaccines_data:
            await vaccine_repository.create(name=vaccine['name'])
        
        # Load and create vaccination point vaccines
        logger.info("Creating vaccination point vaccines relationships...")
        with open(BASE_DIR / 'data' / 'vaccination_point_vaccines.json', 'r', encoding='utf-8') as file:
            vpv_data = json.load(file)
        vpv_repository = VaccinationPointVaccineRepository(database)
        for vpv in vpv_data:
            await vpv_repository.create(
                vaccination_point_id=vpv['vaccination_point_id'],
                vaccine_id=vpv['vaccine_id']
            )
            
        logger.info("All data loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise
    finally:
        await database.disconnect()

if __name__ == "__main__":
    init_database()
    asyncio.run(load_json_data())
    