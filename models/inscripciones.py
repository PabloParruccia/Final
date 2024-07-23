from config.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Inscripciones(Base):

    __tablename__ = 'inscripciones'
    
    id = Column(Integer, primary_key = True, autoincrement='auto')
    fecha_inscripcion = Column(Date, nullable=False)
    evento_id = Column(Integer, ForeignKey('eventos.id'), nullable=False)
    usuario_id =Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship('Usuarios', lazy='joined', back_populates='inscripciones')
    evento = relationship('Eventos', lazy='joined', back_populates='inscripciones')
    
    class Config:
        from_attributes = True