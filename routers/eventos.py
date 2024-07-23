from fastapi import APIRouter, status, Depends, Path, Query, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List, Literal
from pydantic import EmailStr
from schemas.eventos import Eventos 
from services.eventos import EventoService
from config.database import Session
from utils.jwt_manager import get_current_user
from datetime import date

eventos_router = APIRouter()


@eventos_router.post('/Eventos/', tags=['Eventos'],status_code=status.HTTP_201_CREATED,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def new_Eventos(nombre:str=Form(...),descripcion:str=Form(...),fecha_inicio:date=Form(...),fecha_fin:date=Form(...),lugar:str=Form(...),cupos:int=Form(...),categoria_id:int=Form(...)):
    evento=Eventos(
        id=None,
        nombre=nombre,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        lugar=lugar,
        cupos=cupos,
        categoria_id=categoria_id
    )
    db=Session()
    
    EventoService(db).create_evento(evento)
    return JSONResponse(status_code=201, content={"message": "Eventos registrada"})
##Buscar eventos por nombre o descripción.

@eventos_router.get('/Eventos/{nombre}', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def get_Eventos(nombre: str):
    db=Session()
    result = EventoService(db).get_evento_nombre(nombre)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="nombre de Eventos no encontrada" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@eventos_router.get('/Eventos/descripcion/{descripcion}', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def get_Eventos(descripcion: str):
    db=Session()

    result = EventoService(db).get_evento_descripcion(descripcion)

    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Eventos no encontrada" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

# # Obtener la lista de eventos disponibles.
@eventos_router.get('/Eventos/disponibles/{fecha}', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def get_Eventos(fecha : date):
    db=Session()
    result = EventoService(db).get_evento_disponibles(fecha)
    print(result)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Eventos no encontradas" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@eventos_router.get('/Eventos/', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def get_Eventos():
    db=Session()
    result = EventoService(db).get_evento()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No hay Eventos" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@eventos_router.get('/Eventos/id/{id}', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def get_Eventos_id(id: int):
    db=Session()
    result = EventoService(db).get_evento_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Eventos no encontrada" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

	
@eventos_router.put('/Eventos/{id}', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def update_Eventos(id: int ,evento : Eventos):
     db=Session()
     result=EventoService(db).get_evento_id(id)
     if not result:
          raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Eventos no existe." )
     EventoService(db).update_evento(id,evento)
     return JSONResponse(status_code=200,content={"Message":"Eventos modificado correctamente"}) 



@eventos_router.delete('/Eventos/{id}', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def delete_Eventos(id: int): 
    db=Session()
    EventoService(db).delete_evento(id)
    return JSONResponse(status_code=200, content={"message": "Eventos eliminada correctamente"})

@eventos_router.get('/Eventos /{categoria}', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def get_Eventos(categoria: int):
    db=Session()
    result = EventoService(db).get_evento_by_category(categoria)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="nombre de Eventos no encontrada" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


# devuelve la cantidad de eventos para el dashboard
@eventos_router.get('/count/', tags=['Eventos'], status_code=status.HTTP_200_OK,response_model=list[Eventos], dependencies=[Depends(get_current_user)])
def get_Eventos():
    db=Session()
    result = EventoService(db).count_total_eventos()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No hay Eventos o el total es 0" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

