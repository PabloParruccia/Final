from config.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Eventos(Base):

    __tablename__ = 'eventos'

    id = Column(Integer, primary_key = True, autoincrement='auto')
    nombre = Column(String(30), nullable=False)
    descripcion = Column(String(250))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    lugar = Column(String(128), nullable=False)
    cupos = Column(Integer, nullable= False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    categoria = relationship('Categorias', lazy='joined', back_populates='eventos')#guarda los obj que corresponden al id de categoria.
    inscripciones = relationship('Inscripciones', lazy='joined', back_populates='evento')

    class Config:
        from_attributes = True