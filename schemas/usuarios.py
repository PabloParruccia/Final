from fastapi import HTTPException,status,Query,Depends,File,Form
from fastapi.responses import HTMLResponse
from typing import Annotated , Any,Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from fastapi.responses import JSONResponse
from typing import Optional, Literal

class UsuarioBase(BaseModel):
    id:Optional[int|None]=Field(default=None)#esta definido de esta forma para que SQLalchemy nos deje usar el auto_increment.Pero tambien aceptasmos Int.
    nombre:str=Field(title="nombre")
    email:EmailStr=Field(examples=["nombre@gmail.com"])
    rol:Literal['Cliente','Administrador']= Field(default='Cliente', examples=['Cliente | Administrador'])

    class Config:
        from_attributes = False
        orm_mode = True # indica a Pydantic que debe convertir automáticamente los objetos SQLAlchemy en modelos Pydantic.


class Usuario(UsuarioBase):
    hashed_password:str 
    @classmethod
    def mayor_que_cero(cls, v):
            if len(v)<8 :
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="debe ser mayor a 8 caracteres.")
                
            else:
                contadorMayus = 0
                for largo in v :
                    if str(largo).isupper():
                        contadorMayus=+1
                if contadorMayus >= 1 :
                    return JSONResponse(status_code=200, content={"message": "Su contraseña no cumple con los requisitos"})
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail="debe contener a menos una MAYUSCULA.")
            
class Config:
        from_attributes = True

