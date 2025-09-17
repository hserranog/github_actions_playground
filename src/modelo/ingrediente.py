from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    unidad = Column(String)
    valor = Column(Integer)
    sitioCompra = Column(String)

    def __getitem__(self, key):
        """
        Hace que Ingrediente sea un objeto subscriptable.
        Permite el acceso a los atributos usando notacion de diccionario
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' No se encontró objeto en Ingrediente.")