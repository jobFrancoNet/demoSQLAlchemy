from sqlalchemy import create_engine, MetaData, Table,text,Column, Integer, String,Insert,ForeignKey,Boolean
import json
from sqlalchemy.orm import DeclarativeBase, Session,relationship

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

class Cliente(Base):
    __tablename__ = 'clienti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Relazione con Ordine
    ordini = relationship("Ordine", back_populates="cliente", cascade="all, delete-orphan")

# Entità Ordine
class Ordine(Base):
    __tablename__ = 'ordini'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String, nullable=False)
    evaso = Column(Boolean, default=False)
    cliente_id = Column(Integer, ForeignKey('clienti.id'), nullable=False)

    # Relazione inversa con Cliente
    cliente = relationship("Cliente", back_populates="ordini")

#crea struttura tabelle
def crea_struttura(engine):
    try:
        Base.metadata.create_all(engine)
        print("Struttura del database creata con successo.")
    except Exception as e:
        print(f"Errore durante la creazione della struttura: {e}")

#Inserimento dati
# Metodo per inserire dati

def inserisci_dati(session):
    # Inserimento di 5 clienti
    clienti = [
        Cliente(nome="Mario Rossi", email="mario.rossi@example.com"),
        Cliente(nome="Luigi Verdi", email="luigi.verdi@example.com"),
        Cliente(nome="Anna Bianchi", email="anna.bianchi@example.com"),
        Cliente(nome="Paola Neri", email="paola.neri@example.com"),
        Cliente(nome="Giovanni Blu", email="giovanni.blu@example.com")
    ]
    session.add_all(clienti)
    session.commit()

    # Recupero degli ID dei clienti
    clienti = session.query(Cliente).all()

    # Inserimento di 6 ordini
    ordini = [
        Ordine(descrizione="Ordine 1", evaso=False, cliente_id=clienti[0].id),
        Ordine(descrizione="Ordine 2", evaso=False, cliente_id=clienti[1].id),
        Ordine(descrizione="Ordine 3", evaso=False, cliente_id=clienti[2].id),
        Ordine(descrizione="Ordine 4", evaso=False, cliente_id=clienti[3].id),
        Ordine(descrizione="Ordine 5", evaso=False, cliente_id=clienti[4].id),
        Ordine(descrizione="Ordine 6", evaso=False, cliente_id=clienti[0].id)
    ]
    session.add_all(ordini)
    session.commit()

#ordini evasi

def visualizza_ordini_evasi(session):
    from sqlalchemy.orm import joinedload

    ordini_evasi = (
        session.query(Ordine)
        .options(joinedload(Ordine.cliente))
        .filter(Ordine.evaso == False)
        .all()
    )
    for ordine in ordini_evasi:
        print(f"Cliente: {ordine.cliente.nome}, Email: {ordine.cliente.email}, Ordine: {ordine.descrizione}")

# Metodo per visualizzare clienti senza ordini

def visualizza_clienti_senza_ordini(session):
    # Query per selezionare i clienti che non hanno ordini
    clienti_senza_ordini = (
        session.query(Cliente)
        .outerjoin(Ordine)
        .filter(Ordine.id.is_(None))
        .all()
    )
    if clienti_senza_ordini:
        for cliente in clienti_senza_ordini:
            print(f"Cliente: {cliente.nome}, Email: {cliente.email}")
    else:
        print("Non ci sono clienti senza ordini.")

# Metodo per aggiornare le informazioni di un ordine

def aggiorna_ordine(session, ordine_id, nuova_descrizione=None, nuovo_stato=None):
   # ordine = session.query(Ordine).get(ordine_id) #deprecated
   # attuale per la versione 2.x di SQLAlchemy
    ordine = session.get(Ordine, ordine_id)
    if ordine:
        if nuova_descrizione:
            ordine.descrizione = nuova_descrizione
        if nuovo_stato is not None:
            ordine.evaso = nuovo_stato
        session.commit()
        print(f"Ordine {ordine_id} aggiornato con successo.")
    else:
        print(f"Ordine {ordine_id} non trovato.")

class ProcedureResult:
    def __init__(self, Evaso, nome):
        self.nome=nome
        self.Evaso=Evaso



def esegui_spOnServer(Session,idOrdine):
        # Esecuzione della stored procedure
        isql=f"EXEC sp_GetOrdineById {idOrdine}"
        result = Session.execute(
            text(isql))

        # Mappare i risultati
        mapped_results = [
            ProcedureResult(row.Evaso, row.nome) for row in result.fetchall()
        ]
        for item in mapped_results:
            print(item.Evaso, item.nome)


engine=None
engine,stringaconnessione=connessione()
#crea_struttura(engine)
Session=Session(engine)
#inserisci_dati(Session)

#visualizza_ordini_evasi(Session)

#visualizza_clienti_senza_ordini(Session)

#aggiorna_ordine(Session, 6,'Ordine 6 Update',True)

esegui_spOnServer(Session,1)

