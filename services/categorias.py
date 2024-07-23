from models.categorias import Categorias as CategoriaModel
from schemas.categorias import Categoria
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

class CategoriaService():
    
    def __init__(self, db:Session) -> None:
        self.db = db

    def get_categoria(self):
        result = self.db.query(CategoriaModel).all()
        return [Categoria(**result.__dict__) for result in result]

    def get_categoria_id(self, id):
        result = self.db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
        return result


    def create_categoria(self, categoria: Categoria):
        try:
            new_categoria = CategoriaModel(**categoria.dict())
            self.db.add(new_categoria)
            self.db.commit()
            return
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error.')
 
    def update_categoria(self, id: int, data: Categoria):
        categoria = self.db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
        categoria.nombre = data.nombre
        categoria.descripcion = data.descripcion
        self.db.commit()
        return

    def delete_categoria(self, id: int):
        try:
            result = self.db.query(CategoriaModel).filter(CategoriaModel.id == id).delete()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La categoria no existe.")
            self.db.commit()
            return {"message": "Categoría eliminada correctamente."}
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar la categoría porque tiene eventos asociados.")