from sqlalchemy import create_engine
import pyodbc
import json
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


#Test connessione con SQL Alchemy library

engine = create_engine(connection_string_1)
try:
    with engine.connect() as connection:
        print(f"Connessione riuscita! per {connection_string_1}")
except Exception as e:
    print(f"Errore di connessione: {e}")

