
from fastapi import APIRouter, status, Depends, Path, Query, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List, Literal
from pydantic import EmailStr
from schemas.usuarios import Usuario, UsuarioBase 
from services.usuarios import UsuarioServ
from config.database import Session
from utils.jwt_manager import get_current_user
from models.categorias import Categorias as CategoriaModel
from schemas.categorias import Categoria
from services.categorias import CategoriaService


from config.database import Session

Categoria_router = APIRouter()



# CATEGORIA

@Categoria_router.post('/categoria/', tags=['categoria'],status_code=status.HTTP_201_CREATED,response_model=list[Categoria], dependencies=[Depends(get_current_user)])
def new_categoria(nombre:str=Form(...),descripcion:str=Form(...)):
    categoria=Categoria(
        id=None,
        nombre=nombre,
        descripcion=descripcion
    )
    db=Session()
    CategoriaService(db).create_categoria(categoria)
    return JSONResponse(status_code=201, content={"message": "categoria registrada"})

@Categoria_router.get('/categoria/', tags=['categoria'], status_code=status.HTTP_200_OK,response_model=list[Categoria], dependencies=[Depends(get_current_user)])
def get_categoria():
    db=Session()
    result = CategoriaService(db).get_categoria()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existen Categorias" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@Categoria_router.get('/categoria/{id}', tags=['categoria'], status_code=status.HTTP_200_OK,response_model=list[Categoria], dependencies=[Depends(get_current_user)])
def get_categoria(id: int):
    db=Session()
    result = CategoriaService(db).get_categoria_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Categoria no encontrada" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

	
@Categoria_router.put('/categoria/{id}', tags=['categoria'], status_code=status.HTTP_200_OK,response_model=list[Categoria], dependencies=[Depends(get_current_user)])
def update_categoria(id: int ,categoria : Categoria):
     db=Session()
     result=CategoriaService(db).get_categoria_id(id)
     if not result:
          raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="categoria no existe." )
     CategoriaService(db).update_categoria(id,categoria)
     return JSONResponse(status_code=200,content={"Message":"categoria modificado correctamente"}) 



@Categoria_router.delete('/categoria/{id}', tags=['categoria'], status_code=status.HTTP_200_OK,response_model=list[Categoria], dependencies=[Depends(get_current_user)])
def delete_categoria(id: int): 
    db=Session()
    CategoriaService(db).delete_categoria(id)
    return JSONResponse(status_code=200, content={"message": "categoria eliminada correctamente"})

