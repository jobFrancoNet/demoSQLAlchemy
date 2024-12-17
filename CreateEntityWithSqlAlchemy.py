from sqlalchemy import create_engine, MetaData, Table,text,Column, Integer, String,Insert
import json
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    metadata = MetaData()


def connessione():
    engine=None
    with open("connessioneSQL.json", "r") as file:
        config = json.load(file)

    # Estrarre i dati dal file JSON
    db_config = config["sql_server"]
    username = db_config["username"]
    password = db_config["password"]
    server = db_config["server"]
    database = db_config["database"]
    driver = db_config["driver"]

    # Creare la stringa di connessione
    connection_string_1 = f"mssql+pyodbc://{username}:{password}@{driver}"

    # Creazione engine

    engine = create_engine(connection_string_1)


    return engine,connection_string_1




class User(Base):
    __tablename__='users'
    id = Column('id',Integer, primary_key=True)
    name = Column('name',String(50))
    email = Column('email',String(100))


def CreateTable():
    engine,stringaconnessione = connessione()
    Base.metadata.create_all(engine)


def insert_data(data):
    engine,stringaconnessione = connessione()

    with Session(engine) as session:
        try:
            if isinstance(data, list):
                users = [User(**record) for record in data]
                session.add_all(users)
            elif isinstance(data, dict):
                user = User(**data)
                session.add(user)
            else:
                raise ValueError("I dati devono essere un dizionario o una lista di dizionari.")
            session.commit()
            print("Dati inseriti con successo!")
        except Exception as e:
            session.rollback()
            print(f"Errore durante l'inserimento: {e}")



# Creare le tabelle nel database
CreateTable()

# Esempio di inserimento dati
data_to_insert = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]

insert_data(data_to_insert)


