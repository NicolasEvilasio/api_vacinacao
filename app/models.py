from sqlalchemy import JSON, Float, Column, ForeignKey, Integer, String, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
from app.database import metadata

Base = declarative_base(metadata=metadata)


class UnidadeSaude(Base):
    __tablename__ = "unidades_saude"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)
    schedules = Column(JSON, nullable=True)
    full_address = Column(String, nullable=True)
    neighborhood = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    

class Country(Base):
    """Modelo que representa um país no sistema"""
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID único do país")
    name = Column(String, nullable=False, comment="Nome do país")
    ibge_code = Column(String, nullable=True, unique=True, comment="Código IBGE do país")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="Data de criação do registro")

    states = relationship("State", back_populates="country", cascade="all, delete-orphan")
    
    
class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey('countries.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    ibge_code = Column(String, nullable=True, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    country = relationship("Country", back_populates="states")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    state_id = Column(Integer, ForeignKey('states.id'), nullable=False)
    name = Column(String, nullable=False)
    ibge_code = Column(String, nullable=True, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class VaccinationPoint(Base):
    __tablename__ = "vaccination_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    name = Column(String, nullable=False)
    schedules = Column(JSON, nullable=True)
    full_address = Column(String, nullable=True)
    neighborhood = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    
class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
class VaccinationPointVaccine(Base):
    __tablename__ = "vaccination_point_vaccines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vaccination_point_id = Column(Integer, ForeignKey('vaccination_points.id'), nullable=False)
    vaccine_id = Column(Integer, ForeignKey('vaccines.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

