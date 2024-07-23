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
from utils.user import get_password_hash
usuarios_router = APIRouter()

@usuarios_router.get("/usuarios", tags=["usuarios"],status_code=status.HTTP_200_OK, 
                    response_model=List[UsuarioBase], dependencies=[Depends(get_current_user)])
def get_usuarios():
    db = Session()
    result = UsuarioServ(db).get_usuarios()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existen Usuarios" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@usuarios_router.get("/usuarios/{id}", tags=["usuarios"],status_code=status.HTTP_200_OK, 
                    response_model=UsuarioBase, dependencies=[Depends(get_current_user)])
def get_usuario_id(id:int):
    db = Session()
    result = UsuarioServ(db).get_usuario_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existen Usuarios" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@usuarios_router.post("/usuarios", tags=["usuarios"],status_code=status.HTTP_200_OK, 
                     response_model=List[UsuarioBase])
def create_usuario(nombre:str=Form(...), email:EmailStr=Form(...), rol:Literal['Cliente','Administrador']=Form(...), hashed_password:str=Form(...)):
    usuario=Usuario(
        id = None,
        nombre = nombre,
        email = email,
        rol = rol,
        hashed_password = hashed_password)
    
    db = Session()
    Usuario.mayor_que_cero(usuario.hashed_password)
    result = UsuarioServ(db).create_usuario(usuario)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existen Usuarios" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@usuarios_router.put("/usuarios/{id}", tags=['usuarios'], status_code=status.HTTP_200_OK,response_model=list[Usuario], dependencies=[Depends(get_current_user)])
def update_usuario(id : int ,usuario : Usuario) -> dict:
    db = Session()
    result=UsuarioServ(db).get_usuario_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Usuario no existe." ) 
    Usuario.mayor_que_cero(usuario.hashed_password) 
    hashed_password = get_password_hash(usuario.hashed_password)
    usuario.hashed_password = hashed_password
    UsuarioServ(db).update_usuario(id, usuario)
    return JSONResponse(status_code=200, content={"message": "Usuario modificado correctamente"})

@usuarios_router.delete("/usuarios/{id}", tags=["usuarios"],status_code=status.HTTP_200_OK, 
                       response_model=List[UsuarioBase], dependencies=[Depends(get_current_user)])
def elimina_usuario(id:int):
    db = Session()
    result = UsuarioServ(db).delete_usuario(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No existen Usuarios" )
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


