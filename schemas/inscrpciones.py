from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import date

class Inscripciones(BaseModel):
    id:Optional[int|None]=Field(default=None)
    evento_id:int=Field(gt=0,default=1)
    usuario_id:int=Field(gt=0,default=1)
    fecha_inscripcion:date=Field(examples=["2024-01-31"])

    class Config:
        from_attributes = True
