import os
import shutil
from models.usuarios import Usuarios as UsuarioModel
from schemas.usuarios import Usuario, UsuarioBase
from sqlalchemy.orm import Session, load_only
from sqlalchemy.exc import IntegrityError
from utils.user import get_password_hash
from typing import List
from fastapi.exceptions import HTTPException
from fastapi import status, File, UploadFile
from fastapi.responses import FileResponse

class UsuarioServ():
    
    def __init__(self, db:Session) -> None:
        self.db = db
    
    def get_usuarios(self)->UsuarioBase:
        result = self.db.query(UsuarioModel).options( load_only(UsuarioModel.id, UsuarioModel.nombre, UsuarioModel.email, UsuarioModel.rol)).all()
        return [UsuarioBase(**result.__dict__) for result in result]# Iteramos sobre los resultados obtenidos (results) y creamos una lista de objetos UsuarioBase utilizando los datos de cada objeto UsuarioModel.


    def get_usuario_id(self, id:int)->UsuarioBase:
        result = self.db.query(UsuarioModel).filter(UsuarioModel.id == id).options( load_only(UsuarioModel.id, UsuarioModel.nombre, UsuarioModel.email, UsuarioModel.rol)).first()
        return result
    
    #Devuelve la PASSWORD. Se usa en la validación del login.
    def get_usuario_mail(self, email:str)->Usuario:
        result = self.db.query(UsuarioModel).filter(UsuarioModel.email == email).options( load_only(UsuarioModel.id, UsuarioModel.nombre, UsuarioModel.email, UsuarioModel.rol)).first()
        return result
    
    def create_usuario(self, usuario:Usuario):
        try:
            #Pasar usuario como None para usar la función autoincrement de la db.
            usuario.hashed_password = get_password_hash(usuario.hashed_password)
            nuevo_usuario = UsuarioModel(**usuario.model_dump())#genera el dict de pydantic
            self.db.add(nuevo_usuario)
            self.db.commit()
            return {'message':'Usuario creado'}
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'El email {usuario.email} ya se encuentra registrado.')
        
    def update_usuario(self, id:int, nuevo: Usuario):
        usuario = self.db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        usuario.nombre = nuevo.nombre
        usuario.email = nuevo.email
        usuario.rol = nuevo.rol
        usuario.hashed_password = nuevo.hashed_password
        self.db.commit()
        return {'message':'Usuario modificado'}

    def delete_usuario(self, id:int):
        result = self.db.query(UsuarioModel).filter(UsuarioModel.id == id).delete()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'El usuario de id {id} no fue encontrado')
        self.db.commit()
        return {'message':'Usuario eliminado'}
    