from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Categorias(Base):
    
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key = True, autoincrement='auto')
    nombre = Column(String(30), nullable=False)
    descripcion = Column(String(256))

    eventos = relationship('Eventos',lazy='joined', back_populates='categoria')

    class Config:
        from_attributes = True