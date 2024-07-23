from models.eventos import Eventos as EventosModel
from schemas.eventos import Eventos
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError
from services.categorias import CategoriaService
from datetime import datetime, date
from sqlalchemy.orm import Session,load_only,joinedload
from sqlalchemy import func


class EventoService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_evento(self):
        
        result = self.db.query(EventosModel).options(load_only(EventosModel.id,EventosModel.fecha_fin,EventosModel.fecha_inicio,EventosModel.categoria_id,EventosModel.cupos,EventosModel.nombre,EventosModel.descripcion,EventosModel.lugar)).all()
        return [Eventos(**result.__dict__) for result in result]
    

# cosas para el dashboard
    def count_total_eventos(self):
        result = self.db.query(func.count(EventosModel.id)).scalar()
        return result
    


       
#fin de cosas para el dashboard

    def get_evento_id(self, id:int):
        result = self.db.query(EventosModel).filter(EventosModel.id == id).options(
        load_only(EventosModel.id, EventosModel.nombre, EventosModel.descripcion, EventosModel.fecha_inicio, EventosModel.fecha_fin, EventosModel.lugar, EventosModel.cupos, EventosModel.categoria_id)
    ).first()
        return result

    def get_evento_by_category(self, evento):
        result = self.db.query(EventosModel).filter(EventosModel.categoria_id == evento).all()
        return result

    def create_evento(self, evento: Eventos):
        try:
            resultCategoria=CategoriaService(self.db).get_categoria_id(evento.categoria_id)

            if resultCategoria == None :
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La Categoria ingresada no es valida.")
            
            new_evento = EventosModel(**evento.dict())
            self.db.add(new_evento)
            self.db.commit()
            return 
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error.")    
    
    def update_evento(self, id: int, data: Eventos):
        evento = self.db.query(EventosModel).filter(EventosModel.id == id).first()
        evento.nombre = data.nombre
        evento.descripcion = data.descripcion
        evento.fecha_inicio = data.fecha_inicio
        evento.fecha_fin = data.fecha_fin
        evento.lugar = data.lugar
        evento.cupos = data.cupos
        evento.categoria_id = data.categoria_id
        self.db.commit()
        return

    def delete_evento(self, id: int):
        try:
            result = self.db.query(EventosModel).filter(EventosModel.id == id).delete()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El evento no existe.")
            self.db.commit()
        except IntegrityError:
            self.db.rollback()  # Rollback the transaction to avoid partial commits
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar el evento porque tiene inscripciones asociadas.")
        return result
    
    ##Obtener la lista de eventos disponibles.
    def get_evento_disponibles(self, fecha: date):
        result = self.db.query(EventosModel).options(load_only(EventosModel.id,EventosModel.fecha_fin,EventosModel.fecha_inicio,EventosModel.categoria_id,EventosModel.cupos,EventosModel.nombre,EventosModel.descripcion,EventosModel.lugar)).filter(EventosModel.fecha_inicio >= fecha).all()
        return [Eventos(**result.__dict__) for result in result]# Iteramos sobre los resultados obtenidos (results) y creamos una lista de objetos UsuarioBase utilizando los datos de cada objeto UsuarioModel.
    
   
     
    def get_evento_nombre(self, nombre:str):

        result = self.db.query(EventosModel).options(load_only(EventosModel.id,EventosModel.fecha_fin,EventosModel.fecha_inicio,EventosModel.categoria_id,EventosModel.cupos,EventosModel.nombre,EventosModel.descripcion,EventosModel.lugar)).filter(EventosModel.nombre == nombre).all()
        return [Eventos(**result.__dict__) for result in result]
    
    def get_evento_descripcion(self, descripcion: str):
        result = self.db.query(EventosModel).options(load_only(EventosModel.id,EventosModel.fecha_fin,EventosModel.fecha_inicio,EventosModel.categoria_id,EventosModel.cupos,EventosModel.nombre,EventosModel.descripcion,EventosModel.lugar)).filter(EventosModel.descripcion == descripcion).all()
        return [Eventos(**result.__dict__) for result in result]
    
    def get_evento_cupos(self, evento_id: int):
        evento = self.db.query(EventosModel).filter(EventosModel.id == evento_id).first()
        return evento.cupos if evento else None

    def set_eventos_cupos(self, evento_id: int, new_cupos: int):
        evento = self.db.query(EventosModel).filter(EventosModel.id == evento_id).first()
        if evento:
            evento.cupos = new_cupos
            self.db.commit()