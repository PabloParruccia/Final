from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = f"mysql+mysqlconnector://parrucciape:pmg@localhost:3306/tpi_lab_4"

engine = create_engine(DATABASE_URL,
    pool_size=10,  # Ajusta esto según tus necesidades
    max_overflow=20,  # Ajusta esto según tus necesidades
    pool_timeout=30   # Ajusta esto según tus necesidades
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()