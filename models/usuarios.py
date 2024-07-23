from enum import Enum
from config.database import Base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

class Usuarios(Base):

    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key= True, autoincrement='auto')
    nombre = Column(String(50), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    rol = Column(Enum('Administrador','Cliente'), default='Cliente',name='rol')
    hashed_password = Column(String(256), nullable=False)

    inscripciones = relationship('Inscripciones',lazy='joined', back_populates= 'usuario')

    class Config:
        from_attributes = True