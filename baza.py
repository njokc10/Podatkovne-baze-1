import sqlite3
# import pandas as pd
import cars

# db = sqlite3.connect("baza.sqlite3")
# vsebina = pd.read_csv("primer.csv", sep=";", header=0, names=("cena", "barva", "moc_motorja", "poraba"))

seznam_avtomobilov = cars.get_car()

def naredi_tabelo(conn):
    with conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS avto (id INTEGER PRIMARY KEY,
                znamka TEXT,
                model TEXT,
                menjalnik TEXT
            """),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS lastnosti_motorja (id INTEGER PRIMARY KEY,
                pogon TEXT,
                tip VARCHAR,
                stevilo_prestav INTEGER)
            """),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS dimenzije (id INTEGER PRIMARY KEY,
                visina INTEGER,
                dolžina INTEGER,
                sirina INTEGER)
            """),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS specifikacije_motorja (id INTEGER PRIMARY KEY,
                moc INTEGER,
                navor INTEGER,
            """),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS poraba (id INTEGER PRIMARY KEY,
                mestna INTEGER
                avtocestna INTEGER
                gorivo TEXT
            """)

def dodaj_podatke(conn):
    with conn:
        pass

# def dodaj_podatke(conn):
#     with conn:
#         for indeks, vrstica in vsebina.iterrows():
#             cena = vrstica["cena"]
#             barva = vrstica["barva"]
#             moc_motorja = vrstica["moc_motorja"]
#             poraba = vrstica["poraba"]
#             conn.execute(
#                 """
#                 insert into Avto(cena, barva, moc_motorja, poraba) 
#                 values(:cena, :barva, :moc_motorja, :poraba)
#                 """, {"cena":cena, "barva":barva, "moc_motorja":moc_motorja, "poraba":poraba})
    
#         conn.execute(
#             """
#             INSERT INTO Znamka (ime) VALUES ('Hyundai')
#             """
#         )
#         conn.execute(
#             """INSERT INTO Znamka (ime) VALUES ('Alfa Romeo')""")
   
def pripravi_bazo(conn):
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() != (0, ):
            return
    naredi_tabelo(conn)
    dodaj_podatke(conn)