from sqlalchemy import create_engine, MetaData, Table,text
import json

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

def EseguiQuery(connessioneEngineSQL,stringaconnessione,sqlQuery):
     try:
         with connessioneEngineSQL.connect() as connection:
             print(f"Connessione riuscita! per {stringaconnessione}")
             result = connection.execute(text(sqlQuery))
             for row in result:
                 print(row)
             connection.close()
     except Exception as e:
         print(f"Errore: {e}")

engine=None

#configurazione engine leggendo la stringa di connessione da un file JSON
engine,stringaconnessione=connessione();

#ESECUZIONE QUERY DI ESEMPIO
sql_query="Select * from [dbo].[listaPersone]"
EseguiQuery(engine,stringaconnessione,sql_query)



