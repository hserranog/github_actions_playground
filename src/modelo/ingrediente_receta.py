from sqlalchemy import Column, Integer, ForeignKey

from .declarative_base import Base


class IngredienteReceta(Base):
    __tablename__ = 'ingrediente_receta'

    ingrediente_id = Column(
        Integer,
        ForeignKey('ingrediente.id'),
        primary_key=True)

    receta_id = Column(
        Integer,
        ForeignKey('receta.id'),
        primary_key=True)

    cantidad = Column(Integer)