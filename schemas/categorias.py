from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

class Categoria(BaseModel):
    id:Optional[int|None]=Field(default=None)
    nombre:str=Field(title="nombre")
    descripcion:str=Field(title="descripcion")


    class Config:
        from_attributes = False
        orm_mode = True