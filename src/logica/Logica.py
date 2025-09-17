from src.logica.FachadaRecetario import FachadaRecetario
from enum import Enum
import re
import src.modelo.declarative_base as db
from src.modelo.receta import Receta
from src.modelo.ingrediente import Ingrediente
from src.modelo.ingrediente_receta import IngredienteReceta
from sqlalchemy import func


class Errores(Enum):
    ERROR_CAMPO_RECETA = "Se esperaba el campo Receta no vacio y en formato válido. Ejemplo: Arepas"
    ERROR_CAMPO_TIEMPO = "Se esperaba el campo Tiempo de preparación no vacio y en formato válido, Ejemplo: 01:30:00"
    ERROR_CAMPO_PERSONAS = "Se esperaba el campo Número de Personas no vacio y en formato válido. Ejemplo: 4"
    ERROR_CAMPO_CALORIAS = "Se esperaba el campo Calorías por porción no vacio y en formato válido. Ejemplo: 600"
    ERROR_CAMPO_PREPARACION = "Se esperaba el campo Preparación no vacio y en formato válido. Ejemplo: Para preparar Arepa se necesita ..."
    ERROR_ENTRADA_DUPLICADA = "La Receta por agregar ya se encuentra en la base de datos"

class Errores_ingReceta(Enum):
    ERROR_CAMPO_CANTIDAD = "Se esperaba el campo Cantidad no vacio y en formato válido. Ejemplo: 1"
    ERROR_INGREDIENTE_DUPLICADO = "El Ingrediente seleccionado ya se encuentra en la Receta"

class Errores_Ingrediente(Enum):
    ERROR_CAMPO_NOMBRE = "Se esperaba el campo Nombre no vacio y en formato válido. Ejemplo: Azúcar"
    ERROR_CAMPO_UNIDAD = "Se esperaba el campo Unidad no vacio y en formato válido. Ejemplo: Gramo"
    ERROR_CAMPO_VALOR = "Se esperaba el campo Valor no vacio y en formato válido. Ejemplo: 500"
    ERROR_CAMPO_SITIOCOMPRA = "Se esperaba el campo SitioCompra no vacio y en formato válido. Ejemplo: Plaza de Mercado"
    ERROR_ENTRADA_DUPLICADA = "El Ingrediente por agregar ya se encuentra en la base de datos"

class Errores_BorrarIngrediente(Enum):
    ERROR_INGREDIENTE_EXISTE_EN_RECETA = "Ingrediente es parte de por lo menos una Receta por lo tanto no puede ser eliminado"

class Logica(FachadaRecetario):

    def __init__(self):
        db.init_db()

    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        patronTiempo = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"

        if not receta or not isinstance(receta, str):
            return Errores.ERROR_CAMPO_RECETA.value

        if not tiempo or not isinstance(tiempo, str) or not re.match(patronTiempo, tiempo):
            return Errores.ERROR_CAMPO_TIEMPO.value

        try:
            int(personas)
        except:
            return Errores.ERROR_CAMPO_PERSONAS.value

        try:
            int(calorias)
        except:
            return Errores.ERROR_CAMPO_CALORIAS.value

        if not preparacion:
            return Errores.ERROR_CAMPO_PREPARACION.value

        busqueda = db.session.query(Receta).filter(func.lower(Receta.nombre) == receta.strip().lower()).all()
        if len(busqueda) != 0:
            return Errores.ERROR_ENTRADA_DUPLICADA.value

        return ""

    def crear_receta(self, receta, tiempo, personas, calorias, preparacion):
        receta = Receta(
            nombre=receta.strip(),
            tiempo=tiempo.strip(),
            personas=personas,
            calorias=calorias,
            preparacion=preparacion.strip(),
        )
        db.session.add(receta)
        db.session.commit()

    def dar_recetas(self):
        return db.session.query(Receta).order_by(Receta.nombre.asc()).all()

    def dar_receta(self, id_receta):
        return db.session.query(Receta).filter(Receta.id == id_receta).first()

    def dar_ingredientes_receta(self, id_receta):
        query = (
            db.session.query(Receta.nombre, Ingrediente.nombre, Ingrediente.unidad, IngredienteReceta.cantidad)
            .join(IngredienteReceta, Ingrediente.id == IngredienteReceta.ingrediente_id)
            .join(Receta, Receta.id == IngredienteReceta.receta_id)
            .filter(IngredienteReceta.receta_id == id_receta)
            .all()
        )

        # Convertir a lista de diccionarios
        resultado = [
            {"receta": receta, "ingrediente": ingrediente, "unidad": unidad, "cantidad": cantidad}
            for receta, ingrediente, unidad, cantidad in query
        ]

        return resultado

    def dar_ingredientes(self):
        return db.session.query(Ingrediente).all()

    def validar_crear_editar_ingReceta(self, receta, ingrediente, cantidad):
        try:
            int(cantidad)
        except:
            return Errores_ingReceta.ERROR_CAMPO_CANTIDAD.value
        
        if cantidad == "0":
            return Errores_ingReceta.ERROR_CAMPO_CANTIDAD.value

        return ""
    
    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        ingrediente_receta = IngredienteReceta(
            ingrediente_id=ingrediente.id,
            receta_id=receta.id,
            cantidad=cantidad
        )
        db.session.add(ingrediente_receta)
        db.session.commit()

    def eliminar_receta(self, id_receta):
        # Elimina los IngredientesReceta asociados a la Receta
        query = (
            db.session.query(IngredienteReceta)
            .filter(IngredienteReceta.receta_id == id_receta)
            .all()
        )
        for ingrediente_receta in query:
            db.session.delete(ingrediente_receta)

        # Elimina la Receta
        entrada = db.session.query(Receta).get(id_receta)
        db.session.delete(entrada)

        db.session.commit()

    def editar_ingrediente_receta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        ingredienteReceta = (db.session.query(IngredienteReceta)
            .filter(IngredienteReceta.ingrediente_id == ingrediente.id, IngredienteReceta.receta_id == receta.id)
            .first()
        )

        ingredienteReceta.cantidad = cantidad
        db.session.commit()

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra):
        if not nombre or not isinstance(nombre, str):
            return Errores_Ingrediente.ERROR_CAMPO_NOMBRE.value

        if not unidad or not isinstance(unidad, str):
            return Errores_Ingrediente.ERROR_CAMPO_UNIDAD.value

        try:
            int(valor)
        except:
            return Errores_Ingrediente.ERROR_CAMPO_VALOR.value

        if not sitioCompra or not isinstance(sitioCompra, str):
            return Errores_Ingrediente.ERROR_CAMPO_SITIOCOMPRA.value

        busqueda = db.session.query(Ingrediente).filter(func.lower(Ingrediente.nombre) == nombre.strip().lower()).all()
        if len(busqueda) != 0:
            return Errores_Ingrediente.ERROR_ENTRADA_DUPLICADA.value

        return ""

    def crear_ingrediente(self, nombre, unidad, valor, sitioCompra):
        ingrediente = Ingrediente(
            nombre=nombre.strip(),
            unidad=unidad.strip(),
            valor=valor,
            sitioCompra=sitioCompra,
        )
        db.session.add(ingrediente)
        db.session.commit()

    def eliminar_ingrediente(self, id_ingrediente):
        entrada = db.session.query(Ingrediente).get(id_ingrediente)
        if entrada:
            db.session.delete(entrada)
            db.session.commit()

    def validar_eliminar_ingrediente(self, id_ingrediente):
        busqueda = db.session.query(IngredienteReceta).filter(IngredienteReceta.ingrediente_id == id_ingrediente).all()
        if len(busqueda) != 0:
            return Errores_BorrarIngrediente.ERROR_INGREDIENTE_EXISTE_EN_RECETA.value

        return ""