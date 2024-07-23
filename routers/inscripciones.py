from fastapi import APIRouter, status, Depends, Path, Query, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List, Literal
from pydantic import EmailStr
from datetime import date
from schemas.usuarios import Usuario, UsuarioBase 
from services.usuarios import UsuarioServ
from config.database import Session
from utils.jwt_manager import get_current_user

from schemas.inscrpciones import Inscripciones
from services.inscripciones import InscripcionesService


from config.database import Session

inscripciones_router = APIRouter()



# Inscripciones

@inscripciones_router.post('/inscripciones/', tags=['inscripciones'],status_code=status.HTTP_201_CREATED,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def new_inscripciones(evento_id:int=Form(...),usuario_id:int=Form(...),fecha_inscripcion:date=Form(...)):
    inscripciones=Inscripciones(
        id=None,
        evento_id=evento_id,
        usuario_id=usuario_id,
        fecha_inscripcion=fecha_inscripcion
    )
    db=Session()
    InscripcionesService(db).create_inscripciones(inscripciones)
    return JSONResponse(status_code=201, content={"message": "inscripciones registrada"})

## Obtener las inscripciones activas de un usuario.
@inscripciones_router.get('/inscripciones/active', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def get_inscripciones(fecha: date,usuario_id:int):
    db=Session()
    result = InscripcionesService(db).get_inscripciones_usuario(fecha,usuario_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="inscripciones no encontradas" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


## historial de inscripciones del usuario
@inscripciones_router.get('/inscripciones/history/{usuario_id}', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def get_inscripciones(usuario_id: int):
    db=Session()
    result = InscripcionesService(db).get_inscripciones_history_usuario(usuario_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="inscripciones no encontradas" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@inscripciones_router.get('/inscripciones/', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def get_inscripciones():
    db=Session()
    result = InscripcionesService(db).get_inscripciones()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existen Suscripciones" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@inscripciones_router.get('/inscripciones/{id}', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def get_inscripciones(id: int):
    db=Session()
    result = InscripcionesService(db).get_inscripciones_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="inscripciones no encontrada" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

	
@inscripciones_router.put('/minscripciones/{id}', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def update_inscripciones(id: int ,inscripciones : Inscripciones):
     db=Session()
     result=InscripcionesService(db).get_inscripciones_id(id)
     if not result:
          raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="inscripciones no existe." )
     InscripcionesService(db).update_inscripciones(id,inscripciones)
     return JSONResponse(status_code=200,content={"Message":"inscripciones modificado correctamente"}) 



@inscripciones_router.delete('/inscripciones/{id}', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def delete_inscripciones(id: int): 
    db=Session()
    InscripcionesService(db).delete_inscripciones(id)
    return JSONResponse(status_code=200, content={"message": "inscripciones eliminada correctamente"})

## dashboard

@inscripciones_router.get('/inscripciones/count/', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def get_inscripciones_activas():
    db=Session()
    result = InscripcionesService(db).count_inscripciones_activas()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No hay Eventos" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@inscripciones_router.get('/nroinscripevento/', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def get_max_inscripciones():
    db=Session()
    result = InscripcionesService(db).count_max_inscripciones()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No hay Inscripciones a Eventos" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


#Promedio de usuarios
@inscripciones_router.get('/nrouserinsct/', tags=['inscripciones'], status_code=status.HTTP_200_OK,response_model=list[Inscripciones], dependencies=[Depends(get_current_user)])
def get_count_usuario_inscr():
    db=Session()
    result = InscripcionesService(db).promedio_usuarios_inscritos()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No hay Inscripciones a Eventos" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))