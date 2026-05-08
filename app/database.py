from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from urllib.parse import quote_plus

password = quote_plus("%Fermin1234SQL")
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root:{password}@127.0.0.1:3306/reservas_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()