import sqlite3
import pandas as pd

# db = sqlite3.connect("baza.sqlite3")
vsebina = pd.read_csv("primer.csv", sep=";", header=0, names=("cena", "barva", "moc_motorja", "poraba"))

# ustvarjanje_tabel = [
#     """CREATE TABLE IF NOT EXISTS Avto (id INTEGER PRIMARY KEY,
#                 cena INTEGER,
#                 barva TEXT,
#                 moc_motorja TEXT,
#                 poraba FLOAT)""",
#     """CREATE TABLE IF NOT EXISTS Znamka (id INTEGER PRIMARY KEY,
#                 lastnik TEXT)""",
#     """CREATE TABLE IF NOT EXISTS Model (id INTEGER PRIMARY KEY,
#                 oprema TEXT)""",
#     """CREATE TABLE IF NOT EXISTS Pogon (id INTEGER PRIMARY KEY,
#                 tip_pogona TEXT)
#                 """]

# def ustvari_tabele(seznam): 
#     with db as cursor:
#         for tabela in seznam:
#             cursor.execute(tabela)

# if __name__ == "__main__":       
#     ustvari_tabele(ustvarjanje_tabel)

#     with db as cursor:
#         for indeks, vrstica in vsebina.iterrows():
#             cena = vrstica["cena"]
#             barva = vrstica["barva"]
#             moc_motorja = vrstica["moc_motorja"]
#             poraba = vrstica["poraba"]
#             cursor.execute(
#                 """
#                 insert into Avto(cena, barva, moc_motorja, poraba) 
#                 values(:cena, :barva, :moc_motorja, :poraba)
#                 """, {"cena":cena, "barva":barva, "moc_motorja":moc_motorja, "poraba":poraba})





def naredi_tabelo(conn):
    with conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS Avto (id INTEGER PRIMARY KEY,
                cena INTEGER,
                barva TEXT,
                moc_motorja TEXT,
                poraba FLOAT)
            """
        ),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS Znamka (id INTEGER PRIMARY KEY,
                ime TEXT)
            """
        ),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS Model (id INTEGER PRIMARY KEY,
                oprema TEXT)
            """
        ),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS Pogon (id INTEGER PRIMARY KEY,
                tip_pogona TEXT)
            """
        )

def dodaj_podatke(conn):
    with conn:
        for indeks, vrstica in vsebina.iterrows():
            cena = vrstica["cena"]
            barva = vrstica["barva"]
            moc_motorja = vrstica["moc_motorja"]
            poraba = vrstica["poraba"]
            conn.execute(
                """
                insert into Avto(cena, barva, moc_motorja, poraba) 
                values(:cena, :barva, :moc_motorja, :poraba)
                """, {"cena":cena, "barva":barva, "moc_motorja":moc_motorja, "poraba":poraba})
    
        conn.execute(
            """
            INSERT INTO Znamka (ime) VALUES ('Hyundai')
            """
        )

        conn.execute(
            """INSERT INTO Znamka (ime) VALUES ('Alfa Romeo')""")
        


def pripravi_bazo(conn):
    # with conn:
    #     cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
    #     if cur.fetchome() != (0, ):
    #         return
    naredi_tabelo(conn)
    dodaj_podatke(conn)