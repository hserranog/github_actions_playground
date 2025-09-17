import sys
from src.vista.InterfazRecetario import App_Recetario
from src.logica.Logica import Logica

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = Logica()

    app = App_Recetario(sys.argv, logica)
    sys.exit(app.exec_())