from faker.providers import BaseProvider

class RecetasColombia(BaseProvider):
    def receta_nombre_aleatorio(self):
        recetas = [
            "Bandeja paisa",
            "Ajiaco santafereño",
            "Sancocho de gallina",
            "Arepas de queso",
            "Empanadas colombianas",
            "Tamales tolimenses",
            "Lechona huilense",
            "Posta cartagenera",
            "Changua boyacense",
            "Arroz con coco"
        ]
        return self.random_element(recetas)

    def ingrediente_nombre_aleatorio(self):
        ingredientes = [
            "Maíz",
            "Arroz",
            "Fríjoles rojos",
            "Fríjoles cargamanto",
            "Papa criolla",
            "Papa pastusa",
            "Plátano maduro",
            "Plátano verde",
            "Yuca",
            "Arepa de maíz",
            "Carne de res",
            "Carne de cerdo",
            "Pollo",
            "Pescado",
            "Chicharrón",
            "Huevo",
            "Queso costeño",
            "Queso campesino",
            "Cilantro",
            "Aguacate",
            "Cebolla larga",
            "Cebolla cabezona",
            "Ajo",
            "Ají",
            "Leche de coco",
            "Panela",
            "Guayaba",
            "Mango",
            "Lulo",
            "Maracuyá",
            "Arequipe"
        ]
        return self.random_element(ingredientes)

    def unidad_aleatoria(self):
        unidades = [
            "kilogramo",
            "kilo",
            "gramo",
            "litro",
            "mililitro",
            "taza",
            "media taza",
            "cucharada",
            "cucharadita",
            "pizca",
            "pellizco",
            "chorrito",
            "rebanada",
            "rodaja",
            "unidad",
            "pieza"
        ]
        return self.random_element(unidades)
    
    def sitios_de_compra_aleatorio(self):
        sitios_de_compra = [
            "Mercado",
            "Supermercado",
            "Plaza de mercado",
            "Tienda de barrio",
            "Panadería",
            "Carnicería",
            "Pescadería",
            "Frutería",
            "Verdulería",
            "Droguería",
            "Mini mercado",
            "Bodega",
            "Cafetería",
            "Restaurante",
            "Puesto callejero",
            "Puesto de arepas",
            "Puesto de empanadas"
        ]
        return self.random_element(sitios_de_compra)