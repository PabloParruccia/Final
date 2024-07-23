from models.inscripciones import Inscripciones as inscripcionesModel
from schemas.inscrpciones import Inscripciones
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,status
from sqlalchemy.orm import Session,load_only,joinedload
from services.usuarios import UsuarioServ
from services.eventos import EventoService
from models.usuarios import Usuarios as UsuarioModel
from models.eventos import Eventos as EventosModel
from models.categorias import Categorias as CategoriaModel
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy import func
class InscripcionesService():
    
    def __init__(self, db:Session) -> None:
        self.db = db

    def get_inscripciones(self):
        result = self.db.query(inscripcionesModel).options(joinedload(inscripcionesModel.usuario)
                            .load_only(UsuarioModel.id, UsuarioModel.nombre, UsuarioModel.email, UsuarioModel.rol)
                            ).filter().all()
        return result

    def get_inscripciones_id(self, id):
        result = self.db.query(inscripcionesModel).options(joinedload(inscripcionesModel.usuario)
                            .load_only(UsuarioModel.id, UsuarioModel.nombre, UsuarioModel.email, UsuarioModel.rol)
                            ).filter(inscripcionesModel.id == id).first()
        return result

    def count_max_inscripciones(self):
        # Subquery para obtener el evento_id con más inscripciones y su nombre
        subquery = self.db.query(
                        inscripcionesModel.evento_id,
                        EventosModel.nombre.label('nombre_evento'),
                        func.count().label('count_inscripciones')
                    ) \
                    .join(EventosModel, inscripcionesModel.evento_id == EventosModel.id) \
                    .group_by(inscripcionesModel.evento_id, EventosModel.nombre) \
                    .order_by(func.count().desc()) \
                    .limit(1) \
                    .subquery()

        # Consulta principal para obtener el número máximo de inscripciones y el nombre del evento
        result = self.db.query(subquery.c.count_inscripciones, subquery.c.nombre_evento) \
                        .first()

        # Extraer el resultado
        count_max = result.count_inscripciones
        nombre_evento = result.nombre_evento

        return count_max, nombre_evento


    
    def promedio_usuarios_inscritos(self):
        # Subquery para contar las inscripciones por evento
        subquery = self.db.query(inscripcionesModel.evento_id, func.count().label('num_inscripciones')) \
                          .group_by(inscripcionesModel.evento_id) \
                          .subquery()

        # Consulta principal para calcular el promedio de inscripciones
        promedio = self.db.query(func.avg(subquery.c.num_inscripciones).label('promedio_inscripciones')).scalar()

        return promedio


## 


    def get_inscripciones_usuario(self, fecha_actual, usuario_id):
        # Filtrar inscripciones y eventos que no han caducado
        result = self.db.query(inscripcionesModel) \
                        .join(EventosModel, inscripcionesModel.evento_id == EventosModel.id).options(joinedload(inscripcionesModel.usuario)
                            .load_only(
                            ),
                            ).options(load_only( inscripcionesModel.fecha_inscripcion)) \
                        .filter(and_(
                            inscripcionesModel.usuario_id == usuario_id,
                            EventosModel.fecha_inicio <= fecha_actual,
                            EventosModel.fecha_fin >= fecha_actual
                        )) \
                        .all()
        
        return result

    def count_inscripciones_activas(self) -> int:
        fecha_actual = datetime.now().date().strftime('%Y-%m-%d')  # Obtén la fecha actual del sistema
        result = self.db.query(inscripcionesModel).filter(inscripcionesModel.fecha_inscripcion >= fecha_actual).count()
        return result

    def get_inscripciones_history_usuario(self, usuario_id):
        result = self.db.query(inscripcionesModel).options(joinedload(inscripcionesModel.usuario)
                            .load_only(

                            ),
                        load_only(inscripcionesModel.fecha_inscripcion)
                    ).filter(inscripcionesModel.usuario_id == usuario_id).all()
        return result
    # usamos joinedload para cargar la relacion usuario-inscripcion para poder aplicar load_only a las propiedades especificas del modelo usuario y asi no mostrarlas. tambien se podria hacer en evento-inscripcion para no mostralo , de igual manera con la categoria del evento. pero son datos necesarios.
    def create_inscripciones(self, inscripciones: Inscripciones):
        try:
#     
 # Verificar si el usuario ya está registrado en el evento
            existing_inscripcion = self.db.query(inscripcionesModel).filter(
                inscripcionesModel.usuario_id == inscripciones.usuario_id,
                inscripcionesModel.evento_id == inscripciones.evento_id
            ).first()

            if existing_inscripcion:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya se registró a este evento."
                )

            # Verificar que el usuario existe
            result_usuario = UsuarioServ(self.db).get_usuario_id(inscripciones.usuario_id)
            if result_usuario is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El Usuario ingresado no es válido."
                )

            # Verificar que el evento existe
            result_evento = EventoService(self.db).get_evento_id(inscripciones.evento_id)
            if result_evento is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El Evento ingresado no es válido."
                )
            
 # Verificar los cupos disponibles del evento
            result_cupos = EventoService(self.db).get_evento_cupos(inscripciones.evento_id)
            if result_cupos <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya no hay cupos para este evento. Lo siento!"
                )

            # Reducir los cupos en uno
            EventoService(self.db).set_eventos_cupos(inscripciones.evento_id, result_cupos - 1)

            new_inscripciones = inscripcionesModel(**inscripciones.dict())
            self.db.add(new_inscripciones)
            self.db.commit()
            return

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error.")    

    
    def update_inscripciones(self, id: int, data: Inscripciones):
        inscripciones = self.db.query(inscripcionesModel).filter(inscripcionesModel.id == id).first()
        inscripciones.evento_id=data.evento_id
        inscripciones.usuario_id=data.usuario_id
        inscripciones.fecha_inscripcion=data.fecha_inscripcion
        self.db.commit()
        return

    def delete_inscripciones(self, id: int):
       result = self.db.query(inscripcionesModel).filter(inscripcionesModel.id == id).delete()
       if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La inscripcion no existe.")
       self.db.commit()
       return