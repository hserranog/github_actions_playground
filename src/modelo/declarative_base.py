from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Globales
engine = None
Session = None
session = None

def init_db(db_url='sqlite:///aplicacion.sqlite', echo=False):
    """
    Inicializa la conexión a la Base de Datos
    Para Unit Testing usar "sqlite:///:memory:" u otra DB que no sea la de prod
    """
    global engine, Session, session
    
    # Solo inicializa la DB una vez
    if session is not None:
        return session

    engine = create_engine(db_url, echo=echo)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session

def close_db():
    """
    Cierra la Base de Datos
    """
    global engine, Session, session

    session.close()

    engine = None
    Session = None
    session = None
