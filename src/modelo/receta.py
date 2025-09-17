from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Receta(Base):
    __tablename__ = 'receta'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tiempo = Column(String)
    personas = Column(Integer)
    calorias = Column(Integer)
    preparacion = Column(String)

    def __getitem__(self, key):
        """
        Hace que Receta sea un objeto subscriptable.
        Permite el acceso a los atributos usando notacion de diccionario
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' No se encontró objeto en Receta.")