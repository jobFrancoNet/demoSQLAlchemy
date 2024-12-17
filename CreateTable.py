from sqlalchemy import create_engine, MetaData, Table,text,Column, Integer, String,Insert
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

engine=None

engine,stringaconnessione=connessione();


class Descrizioni():
    def __init__(self,nometabella,engine):
       self.tableName=nometabella
       self.__tablename__='Descrizioni'
       self.id = Column('id',Integer, primary_key=True)
       self.name = Column('name',String)
       meta=MetaData()
       Table(self.tableName,meta,self.id,self.name)
       meta.create_all(engine)



def CreateTable(nometabella,engine):
    Descrizioni(nometabella,engine)

def InsertIntoTable(nometabella,engine):
    metadata=MetaData()
    _table_=Table(nometabella, metadata, autoload_with=engine)
    return _table_


# Base per la definizione delle classi ORM
CreateTable("Descrizioni",engine)

tabellaDescrizioni=InsertIntoTable("Descrizioni",engine)

#crea sql statement insert
sqlInsert=Insert(tabellaDescrizioni).values(name='Banco frigorifero')

sqlInsert1=Insert(tabellaDescrizioni).values(name='HP I7 16 GB')

sqlInsert2=Insert(tabellaDescrizioni).values(name='HP I7 32 GB')

try:
    with engine.connect() as connection:
        print(f"Connessione riuscita! per {stringaconnessione}")
        connection.execute(sqlInsert)
        connection.execute(sqlInsert1)
        connection.execute(sqlInsert2)
        connection.commit()
        connection.close()
except Exception as e:
    print(f"Errore: {e}")

