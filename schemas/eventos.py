from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import date

class Eventos(BaseModel):

 
    id:Optional[int|None]=Field(default=None)
    nombre:str=Field(title="nombre")
    descripcion:str=Field(title="descripcion")
    fecha_inicio:date=Field(examples=["2024-01-31"])
    fecha_fin:date=Field(examples=["2024-01-31"])
    lugar:str=Field(title="descripcion")
    cupos :int=Field(gt=0)
    categoria_id :int=Field(gt=0,default=1)

    class Config:
        from_attributes = True#genera un obj a partir de los datos de la bd
