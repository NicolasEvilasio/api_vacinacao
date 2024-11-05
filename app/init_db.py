from sqlalchemy import create_engine
from app.models import Base
from app.database import DATABASE_URL

def init_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_database()
    print("Banco de dados inicializado com sucesso!")