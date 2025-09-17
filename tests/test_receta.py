import unittest
from enum import Enum
from faker import Faker
from tests.faker_datos import RecetasColombia

from src.logica.Logica import Logica
import src.modelo.declarative_base as db
from src.modelo.receta import Receta
from src.modelo.ingrediente import Ingrediente
from src.modelo.ingrediente_receta import IngredienteReceta


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


class RecetaTestCase(unittest.TestCase):

    def setUp(self):
        # Inicializar Base de Datos temporal
        db.init_db("sqlite:///:memory:")
        self.logica = Logica()
        # Generación de datos con libreria Faker
        self.faker = Faker('es_CO')
        self.faker.add_provider(RecetasColombia)

    def tearDown(self):
        # Cerrar sesión con la Base de Datos
        db.close_db()
        self.logica = None

    def test_valida_ningun_campo_vacio(self):
        """
        Valida ninguno de los campos se encuentre vacio
        """
        # ERROR_CAMPO_RECETA vacio
        error_esperado = Errores.ERROR_CAMPO_RECETA.value

        test = {
            "id_receta": -1,
            "receta": "",
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

        # ERROR_CAMPO_TIEMPO vacio
        error_esperado = Errores.ERROR_CAMPO_TIEMPO.value

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": "",
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

        # ERROR_CAMPO_PERSONAS vacio
        error_esperado = Errores.ERROR_CAMPO_PERSONAS.value

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": "",
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

        # ERROR_CAMPO_CALORIAS vacio
        error_esperado = Errores.ERROR_CAMPO_CALORIAS.value

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": "",
            "preparacion": self.faker.text(),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

        # ERROR_CAMPO_PREPARACION vacio
        error_esperado = Errores.ERROR_CAMPO_PREPARACION.value

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": "",
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

    def test_valida_tipo_campo_receta_nombre_aleatorio(self):
        """
        Valida el campo receta sea un String
        """
        error_esperado = Errores.ERROR_CAMPO_RECETA.value

        test = {
            "id_receta": -1,
            "receta": self.faker.random_int(1, 5),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

    def test_valida_tipo_campo_numero_personas(self):
        """
        Valida el campo Números de personas sea un Integer
        """
        error_esperado = Errores.ERROR_CAMPO_PERSONAS.value

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.word(),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

    def test_valida_tipo_campo_calorias_porcion(self):
        """
        Valida el campo Calorías por porción sea un Integer
        """
        error_esperado = Errores.ERROR_CAMPO_CALORIAS.value

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.word(),
            "preparacion": self.faker.text(),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

    def test_valida_formato_campo_tiempo_de_preparacion(self):
        """
        Valida el campo Tiempo de preparación
        """
        error_esperado = Errores.ERROR_CAMPO_TIEMPO.value

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.word(),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": "::00",
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": "1s:00:00",
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, error_esperado)

    def test_valida_receta_ok(self):
        """
        Caso donde todas las validaciónes pasan correctamente
        """
        resultado_esperado = ""

        test = {
            "id_receta": -1,
            "receta": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": str(self.faker.random_int(1, 5)),
            "calorias": str(self.faker.random_int(1, 1000)),
            "preparacion": self.faker.text(),
        }

        resultado = self.logica.validar_crear_editar_receta(**test)
        self.assertEqual(resultado, resultado_esperado)

    def test_crear_receta_ok(self):
        """
        Valida la Receta se agregue normalmente y sin errores
        """
        resultado_esperado = self.faker.receta_nombre_aleatorio()

        test = {
            "receta": resultado_esperado,
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": str(self.faker.random_int(1, 5)),
            "calorias": str(self.faker.random_int(1, 1000)),
            "preparacion": self.faker.text(),
        }
        self.logica.crear_receta(**test)
        consulta = db.session.query(Receta).filter(Receta.nombre == test["receta"]).first()
        resultado = consulta.nombre
        self.assertEqual(resultado, resultado_esperado)

    def test_valida_espacios_en_blanco_son_removidos_al_agregar_receta(self):
        """
        Valida los espacios en blanco son removido al inicio y al final de los campos
        antes de ser agregados a la Base de Datos
        """
        resultado_esperado = self.faker.receta_nombre_aleatorio()

        test = {
            "receta": f"       {resultado_esperado}       ",
            "tiempo": f'       {self.faker.time(pattern="%H:%M:%S")}       ',
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": f"       {self.faker.text()}       ",
        }
        self.logica.crear_receta(**test)
        consulta = db.session.query(Receta).filter(Receta.nombre == resultado_esperado).first()
        self.assertEqual(consulta.nombre, test["receta"].strip())
        self.assertEqual(consulta.tiempo, test["tiempo"].strip())
        self.assertEqual(consulta.preparacion, test["preparacion"].strip())

    def test_valida_error_en_entrada_duplicada(self):
        """
        Valida error al intentar agregar un nombre de Receta ya existente
        No se distingue entre mayúsculas y minúsculas por lo que
        "Pozole" y "pozole" se considera una entrada duplicada.
        Se deben además los espacios en blando al inicio y final en el nombre de la receta
        """
        error_esperado = Errores.ERROR_ENTRADA_DUPLICADA.value

        receta = Receta(
            nombre="Pozole",
            tiempo=self.faker.time(pattern="%H:%M:%S"),
            personas=self.faker.random_int(1, 6),
            calorias=self.faker.random_int(100, 500),
            preparacion=self.faker.text(max_nb_chars=50),
        )
        db.session.add(receta)
        db.session.commit()

        test = {
            "id_receta": -1,
            "receta": "        pozole       ",
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 6),
            "calorias": self.faker.random_int(100, 500),
            "preparacion": self.faker.text(max_nb_chars=50),
        }
        resultado = self.logica.validar_crear_editar_receta(**test)

        self.assertEqual(resultado, error_esperado)

    def test_valida_listar_recetas_ok(self):
        """
        Valida las Recetas son Listadas
        """
        recetas = [
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
        ]
        db.session.add_all(recetas)
        db.session.commit()

        resultado = self.logica.dar_recetas()
        cantidad_de_recetas_esperadas = len(recetas)
        cantidad_de_recetas_obtenidas = len(resultado)
        self.assertEqual(cantidad_de_recetas_obtenidas, cantidad_de_recetas_esperadas)

    def test_valida_listar_recetas_en_orden_alfabetico(self):
        """
        Valida las Recetas son Listadas en orden alfabético
        """

        recetas = [
            Receta(
                nombre="cPozole",
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre="bArepas",
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre="aCarne Asado",
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
        ]
        db.session.add_all(recetas)
        db.session.commit()

        resultado = self.logica.dar_recetas()
        self.assertEqual(resultado[0]["nombre"], recetas[2]["nombre"])
        self.assertEqual(resultado[1]["nombre"], recetas[1]["nombre"])
        self.assertEqual(resultado[2]["nombre"], recetas[0]["nombre"])

    def test_valida_receta_listada_sea_subscriptable(self):
        """
        Valida que los atributos en las recetas listadas se puedan
        acceder usando la notación de corchetes para satisfacer
        la notación del código existendes en las Vistas.

        En otras palabras tiene que comportarse como un Diccionario
        """
        recetas = [
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
        ]
        db.session.add_all(recetas)
        db.session.commit()

        resultado = self.logica.dar_recetas()
        for receta in resultado:
            self.assertIsInstance(receta["nombre"], str, "Esperamos un String")

    def test_valida_dar_receta_especifica(self):
        """
        Valida la funcionalidad del método dar_receta(id_receta)
        """
        resultado_esperado = "Arepas"

        recetas = [
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre="Arepas",
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 6),
                calorias=self.faker.random_int(100, 500),
                preparacion=self.faker.text(max_nb_chars=50),
            ),
        ]

        db.session.add_all(recetas)
        db.session.commit()

        resultado = self.logica.dar_receta(2)

        self.assertEqual(resultado.nombre, resultado_esperado)

    def test_valida_listar_ingredientes_en_recetas(self):
        """
        Valida que los Ingredientes de una Receta sean listados con
        nombre, unidad y cantidad
        """
        ingredientes_esperados = [
            {"receta": "Pozole", "ingrediente": "maiz", "unidad": "kilos", "cantidad": 1},
            {"receta": "Pozole", "ingrediente": "carne", "unidad": "kilos", "cantidad": 2},
            {"receta": "Pozole", "ingrediente": "guajillo", "unidad": "gramos", "cantidad": 3},
            {"receta": "Pozole", "ingrediente": "lechuga", "unidad": "gramos", "cantidad": 3},
        ]

        recetas = [
            Receta(
                nombre="Pozole",
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 5),
                calorias=self.faker.random_int(1, 1000),
                preparacion=self.faker.text(),
            ),
            Receta(
                nombre=self.faker.receta_nombre_aleatorio(),
                tiempo=self.faker.time(pattern="%H:%M:%S"),
                personas=self.faker.random_int(1, 5),
                calorias=self.faker.random_int(1, 1000),
                preparacion=self.faker.text(),
            ),
        ]

        ingredientes = [
            Ingrediente(nombre="maiz", unidad="kilos", valor=1, sitioCompra=self.faker.word()),
            Ingrediente(nombre="carne", unidad="kilos", valor=2, sitioCompra=self.faker.word()),
            Ingrediente(nombre="guajillo", unidad="gramos", valor=3, sitioCompra=self.faker.word()),
            Ingrediente(nombre="lechuga", unidad="gramos", valor=3, sitioCompra=self.faker.word()),
            Ingrediente(nombre=self.faker.ingrediente_nombre_aleatorio(), unidad=self.faker.unidad_aleatoria(), valor=self.faker.random_int(1, 5), sitioCompra=self.faker.word()),
            Ingrediente(nombre=self.faker.ingrediente_nombre_aleatorio(), unidad=self.faker.unidad_aleatoria(), valor=self.faker.random_int(1, 5), sitioCompra=self.faker.word()),
            Ingrediente(nombre=self.faker.ingrediente_nombre_aleatorio(), unidad=self.faker.unidad_aleatoria(), valor=self.faker.random_int(1, 5), sitioCompra=self.faker.word()),
        ]

        ingredientes_recetas = [
            IngredienteReceta(ingrediente_id=1, receta_id=1, cantidad=1),
            IngredienteReceta(ingrediente_id=2, receta_id=1, cantidad=2),
            IngredienteReceta(ingrediente_id=3, receta_id=1, cantidad=3),
            IngredienteReceta(ingrediente_id=4, receta_id=1, cantidad=3),
            IngredienteReceta(ingrediente_id=5, receta_id=2, cantidad=5),
            IngredienteReceta(ingrediente_id=6, receta_id=2, cantidad=4),
            IngredienteReceta(ingrediente_id=7, receta_id=2, cantidad=7),
        ]

        db.session.add_all(recetas)
        db.session.add_all(ingredientes)
        db.session.add_all(ingredientes_recetas)
        db.session.commit()

        resultado = self.logica.dar_ingredientes_receta(1)

        self.assertEqual(len(resultado), len(ingredientes_esperados))

        for esperado in ingredientes_esperados:
            self.assertIn(esperado, resultado)

    def test_dar_ingredientes_ok(self):
        """
        Valida método dar_ingredientes()
        """
        ingredientes_esperados = ["maiz", "carne", "guajillo"]

        ingredientes = [
            Ingrediente(
                nombre=nombre,
                unidad=self.faker.unidad_aleatoria(),
                valor=self.faker.random_int(1, 5),
                sitioCompra=self.faker.sitios_de_compra_aleatorio()
            )
            for nombre in ingredientes_esperados
        ]

        db.session.add_all(ingredientes)
        db.session.commit()

        respuesta = self.logica.dar_ingredientes()

        for entrada in respuesta:
            self.assertIn(entrada["nombre"], ingredientes_esperados)

    def test_validar_crear_editar_ingReceta_ok(self):
        """
        Valida método validar_crear_editar_ingReceta()
        """
        resultado_esperado = ""

        datos_receta = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        test = {
            "receta": Receta(**datos_receta),
            "ingrediente": Ingrediente(**datos_ingrediente),
            "cantidad": self.faker.random_int(1, 5),
        }

        resultado = self.logica.validar_crear_editar_ingReceta(**test)
        self.assertEqual(resultado, resultado_esperado)

    def test_validar_crear_editar_ingReceta_campo_cantidad_no_vacio(self):
        """
        Valida método validar_crear_editar_ingReceta() no tenga el campo cantidad vacio
        """
        resultado_esperado = Errores_ingReceta.ERROR_CAMPO_CANTIDAD.value

        datos_receta = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        test = {
            "receta": Receta(**datos_receta),
            "ingrediente": Ingrediente(**datos_ingrediente),
            "cantidad": "",
        }

        resultado = self.logica.validar_crear_editar_ingReceta(**test)
        self.assertEqual(resultado, resultado_esperado)

    def test_validar_crear_editar_ingReceta_campo_cantidad_no_es_entero(self):
        """
        Valida método validar_crear_editar_ingReceta() de error al no entregarsele un Integer
        """
        resultado_esperado = Errores_ingReceta.ERROR_CAMPO_CANTIDAD.value

        datos_receta = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        test = {
            "receta": Receta(**datos_receta),
            "ingrediente": Ingrediente(**datos_ingrediente),
            "cantidad": self.faker.word(),
        }

        resultado = self.logica.validar_crear_editar_ingReceta(**test)
        self.assertEqual(resultado, resultado_esperado)

    def test_validar_crear_editar_ingReceta_campo_cantidad_no_es_cero(self):
        """
        Valida método validar_crear_editar_ingReceta() de error al usar cero como entrada
        """
        resultado_esperado = Errores_ingReceta.ERROR_CAMPO_CANTIDAD.value

        datos_receta = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        test = {
            "receta": Receta(**datos_receta),
            "ingrediente": Ingrediente(**datos_ingrediente),
            "cantidad": "0",
        }

        resultado = self.logica.validar_crear_editar_ingReceta(**test)
        self.assertEqual(resultado, resultado_esperado)

    def test_validar_crear_editar_ingReceta_ingrediente_ingrediente_se_encuentra_en_otra_receta(self):
        """
        Valida método validar_crear_editar_ingReceta()
        El ingrediente es parte de una receta distinta y no deberia dar error
        """
        resultado_esperado = ""

        datos_receta1 = {
            "nombre": self.faker.unique.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente1 = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        datos_receta2 = {
            "nombre": self.faker.unique.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente2 = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        receta1 = Receta(**datos_receta1)
        ingrediente1 = Ingrediente(**datos_ingrediente1)

        receta2 = Receta(**datos_receta2)
        ingrediente2 = Ingrediente(**datos_ingrediente2)

        crear_data = [
            receta1,
            ingrediente1,
            IngredienteReceta(ingrediente_id=1, receta_id=1, cantidad=self.faker.random_int(1, 5)),

            receta2,
            ingrediente2,
            IngredienteReceta(ingrediente_id=2, receta_id=2, cantidad=self.faker.random_int(1, 5)),
        ]

        db.session.add_all(crear_data)
        db.session.commit()

        test = {
            "receta": receta1,
            "ingrediente": ingrediente2,
            "cantidad": f"{str(self.faker.random_int(1, 5))}",
        }

        resultado = self.logica.validar_crear_editar_ingReceta(**test)
        self.assertEqual(resultado, resultado_esperado)

    def test_agregar_ingrediente_receta_ok(self):
        """
        Valida método agregar_ingrediente_receta()
        """
        datos_receta = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        receta = Receta(**datos_receta)
        ingrediente = Ingrediente(**datos_ingrediente)

        crear_data = [receta, ingrediente]

        db.session.add_all(crear_data)
        db.session.commit()

        cantidad = self.faker.random_int(1, 5)
        self.logica.agregar_ingrediente_receta(receta, ingrediente, cantidad)

        query = (
            db.session.query(Ingrediente.nombre)
            .join(IngredienteReceta, Ingrediente.id == IngredienteReceta.ingrediente_id)
            .join(Receta, Receta.id == IngredienteReceta.receta_id)
            .filter(Ingrediente.nombre == ingrediente["nombre"], Receta.nombre == receta["nombre"])
            .first()
        )

        self.assertIsNotNone(query)

    def test_eliminar_receta_ok(self):
        """
        Prueba el método eliminar_receta() funciene correctamente
        """
        resultado_esperado = 1

        datos_receta1 = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente1 = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        datos_receta2 = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente2 = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        receta1 = Receta(**datos_receta1)
        ingrediente1 = Ingrediente(**datos_ingrediente1)

        receta2 = Receta(**datos_receta2)
        ingrediente2 = Ingrediente(**datos_ingrediente2)

        crear_data = [
            receta1,
            ingrediente1,
            IngredienteReceta(ingrediente_id=1, receta_id=1, cantidad=self.faker.random_int(1, 5)),

            receta2,
            ingrediente2,
            IngredienteReceta(ingrediente_id=2, receta_id=2, cantidad=self.faker.random_int(1, 5)),
        ]

        db.session.add_all(crear_data)
        db.session.commit()

        self.logica.eliminar_receta(1)
        recetas = db.session.query(Receta).all()
        self.assertEqual(len(recetas), resultado_esperado)

    def test_eliminar_receta_con_ingredientes_asociados(self):
        """
        Prueba el método eliminar_receta() funciene correctamente
        """
        resultado_esperado = 3

        datos_receta = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        recetas = [Receta(**datos_receta) for _ in range(2)]
        ingredientes = [Ingrediente(**datos_ingrediente) for _ in range(7)]

        ingredientes_recetas = [
            IngredienteReceta(ingrediente_id=1, receta_id=1, cantidad=1),
            IngredienteReceta(ingrediente_id=2, receta_id=1, cantidad=2),
            IngredienteReceta(ingrediente_id=3, receta_id=1, cantidad=3),
            IngredienteReceta(ingrediente_id=4, receta_id=1, cantidad=3),
            IngredienteReceta(ingrediente_id=5, receta_id=2, cantidad=5),
            IngredienteReceta(ingrediente_id=6, receta_id=2, cantidad=4),
            IngredienteReceta(ingrediente_id=7, receta_id=2, cantidad=7),
        ]

        db.session.add_all(recetas)
        db.session.add_all(ingredientes)
        db.session.add_all(ingredientes_recetas)
        db.session.commit()

        self.logica.eliminar_receta(1)
        ingredientes_en_recetas = db.session.query(IngredienteReceta).all()
        self.assertEqual(len(ingredientes_en_recetas), resultado_esperado)

    def test_validar_editar_ingrediente_receta(self):
        """
        Valida método validar_crear_editar_ingReceta()
        Se intenta editar el ingrediente de una receta
        """
        resultado_esperado = ""

        datos_receta1 = {
            "nombre": self.faker.unique.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente1 = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        receta1 = Receta(**datos_receta1)
        ingrediente1 = Ingrediente(**datos_ingrediente1)

        editar_data = [
            receta1,
            ingrediente1,
            IngredienteReceta(ingrediente_id=1, receta_id=1, cantidad=self.faker.random_int(1, 5)),
        ]

        db.session.add_all(editar_data)
        db.session.commit()

        test = {
            "receta": receta1,
            "ingrediente": ingrediente1,
            "cantidad": f"{str(self.faker.random_int(1, 5))}",
        }

        resultado = self.logica.validar_crear_editar_ingReceta(**test)
        self.assertEqual(resultado, resultado_esperado)

    def test_editar_ingrediente_receta(self):
        """
        Valida método editar_ingrediente_receta()
        """
        datos_receta1 = {
            "nombre": self.faker.unique.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente1 = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        receta1 = Receta(**datos_receta1)
        ingrediente1 = Ingrediente(**datos_ingrediente1)

        editar_data = [
            receta1,
            ingrediente1,
            IngredienteReceta(ingrediente_id=1, receta_id=1, cantidad=3),
        ]

        db.session.add_all(editar_data)
        db.session.commit()

        nuevaCantidad = 5
        test = {
            "id_ingrediente_receta": 1,
            "receta": receta1,
            "ingrediente": ingrediente1,
            "cantidad": nuevaCantidad,
        }
        self.logica.editar_ingrediente_receta(**test)

        query = (
            db.session.query(Ingrediente.nombre)
            .join(IngredienteReceta, Ingrediente.id == IngredienteReceta.ingrediente_id)
            .join(Receta, Receta.id == IngredienteReceta.receta_id)
            .filter(Ingrediente.id == 1, Receta.id == 1, IngredienteReceta.cantidad == nuevaCantidad)
            .first()
        )

        self.assertIsNotNone(query)

    def test_valida_ningun_campo_vacio_agregar_ingrediente(self):
        """
        Valida ninguno de los campos se encuentre vacio
        """
        # ERROR_CAMPO_NOMBRE vacio
        error_esperado = Errores_Ingrediente.ERROR_CAMPO_NOMBRE.value
        test = {
            "nombre": "",
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(100, 500),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }
        resultado = self.logica.validar_crear_editar_ingrediente(**test)
        self.assertEqual(resultado, error_esperado)

        # ERROR_CAMPO_UNIDADA vacio
        error_esperado = Errores_Ingrediente.ERROR_CAMPO_UNIDAD.value
        test = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": "",
            "valor": self.faker.random_int(100, 500),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }
        resultado = self.logica.validar_crear_editar_ingrediente(**test)
        self.assertEqual(resultado, error_esperado)

        # ERROR_CAMPO_valor vacio
        error_esperado = Errores_Ingrediente.ERROR_CAMPO_VALOR.value
        test = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": "",
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }
        resultado = self.logica.validar_crear_editar_ingrediente(**test)
        self.assertEqual(resultado, error_esperado)

        # ERROR_CAMPO_SITIOCOMPRA vacio
        error_esperado = Errores_Ingrediente.ERROR_CAMPO_SITIOCOMPRA.value
        test = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(100, 500),
            "sitioCompra": "",
        }
        resultado = self.logica.validar_crear_editar_ingrediente(**test)
        self.assertEqual(resultado, error_esperado)

    def test_valida_agregar_ingrediente_ok(self):
        """
        Caso donde todas las validaciónes pasan correctamente
        """
        error_esperado = ""
        test = {
            "nombre": self.faker.unique.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(100, 500),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }
        resultado = self.logica.validar_crear_editar_ingrediente(**test)
        self.assertEqual(resultado, error_esperado)

    def test_crear_ingrediente_ok(self):
        """
        Valida el Ingrediente se agregue normalmente y sin errores
        """
        resultado_esperado = self.faker.unique.ingrediente_nombre_aleatorio()

        test = {
            "nombre": resultado_esperado,
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(100, 500),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }
        self.logica.crear_ingrediente(**test)
        consulta = db.session.query(Ingrediente).filter(Ingrediente.nombre == resultado_esperado).first()
        resultado = consulta.nombre
        self.assertEqual(resultado, resultado_esperado)

    def test_crear_ingrediente_duplicado(self):
        """
        Valida el Ingrediente duplicado por el nombre
        """
        error_esperado = Errores_Ingrediente.ERROR_ENTRADA_DUPLICADA.value
        nombre=self.faker.unique.ingrediente_nombre_aleatorio()
        unidad=self.faker.unidad_aleatoria()
        valor=self.faker.random_int(100, 500)
        sitioCompra=self.faker.sitios_de_compra_aleatorio()

        self.logica.crear_ingrediente(nombre,unidad,valor,sitioCompra)

        resultado = self.logica.validar_crear_editar_ingrediente(nombre,unidad,valor,sitioCompra)
        self.assertEqual(error_esperado,resultado)

    def test_eliminar_ingrediente_ok(self):
        """
        Prueba eliminar_ingrediente funcione correctamente
        """
        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }
        db.session.add(Ingrediente(**datos_ingrediente))
        db.session.commit()

        # Ingrediente fue creado en la Base de Datos
        ingrediente_antes = db.session.query(Ingrediente).filter(Ingrediente.id == 1).first()
        self.assertIsNotNone(ingrediente_antes)
        self.assertEqual(ingrediente_antes.nombre, datos_ingrediente["nombre"])

        # Eliminar Ingrediente
        self.logica.eliminar_ingrediente(1)

        # Verificar Ingrediente haya sido eliminado
        ingrediente_despues = db.session.query(Ingrediente).filter(Ingrediente.id == 1).first()
        self.assertIsNone(ingrediente_despues)

    def test_eliminar_ingrediente_no_existente(self):
        """
        Prueba eliminar un ingrediente que no existe en la Base de Datos
        """
        # No deberiamos de encontrarnos con una Exception
        self.logica.eliminar_ingrediente(999)

        # Verificar no hay Ingrediente alguno en la Base de Datos
        ingredientes = db.session.query(Ingrediente).all()
        self.assertEqual(len(ingredientes), 0)

    def test_validar_eliminar_ingrediente_error_ingrediente_existe_en_receta(self):
        """
        Prueba validar_eliminar_ingrediente alerte de error al internar
        eliminar un Ingrediente que se encuentra en por lo mnos una receta
        """
        error_esperado = Errores_BorrarIngrediente.ERROR_INGREDIENTE_EXISTE_EN_RECETA.value

        datos_receta = {
            "nombre": self.faker.receta_nombre_aleatorio(),
            "tiempo": self.faker.time(pattern="%H:%M:%S"),
            "personas": self.faker.random_int(1, 5),
            "calorias": self.faker.random_int(1, 1000),
            "preparacion": self.faker.text(),
        }

        datos_ingrediente = {
            "nombre": self.faker.ingrediente_nombre_aleatorio(),
            "unidad": self.faker.unidad_aleatoria(),
            "valor": self.faker.random_int(1, 5),
            "sitioCompra": self.faker.sitios_de_compra_aleatorio(),
        }

        receta = Receta(**datos_receta)
        ingrediente = Ingrediente(**datos_ingrediente)

        crear_data = [
            receta,
            ingrediente,
            IngredienteReceta(ingrediente_id=1, receta_id=1, cantidad=self.faker.random_int(1, 5))
        ]

        db.session.add_all(crear_data)
        db.session.commit()
        
        # Verifica que la relacion exista
        ing_recetas_antes = db.session.query(IngredienteReceta).filter(
            IngredienteReceta.ingrediente_id == 1
        ).all()
        self.assertEqual(len(ing_recetas_antes), 1)

        # Validar eliminar Ingrediente
        resultado = self.logica.validar_eliminar_ingrediente(1)

        # Verificar mensaje de error
        self.assertEqual(resultado, error_esperado)
