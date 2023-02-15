import pandas as pd

vsebina = pd.read_csv("primer.csv", sep=";", header=0, names=("cena", "barva", "moc_motorja", "poraba"))

def naredi_tabelo(conn):
    '''Ustvarimo tabele'''
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
        ),
        conn.execute(
            """CREATE TABLE IF NOT EXISTS uporabnik (
                uporabniskoIme TEXT,
                geslo TEXT)
            """
        )


def dodaj_podatke(conn):
    '''Dodamo podatke v tabelo'''
    with conn:
        for indeks, vrstica in vsebina.iterrows():
            cena = vrstica["cena"]
            barva = vrstica["barva"]
            moc_motorja = vrstica["moc_motorja"]
            poraba = vrstica["poraba"]
            conn.execute(
                """
                INSERT INTO Avto(cena, barva, moc_motorja, poraba) 
                VALUES(:cena, :barva, :moc_motorja, :poraba)
                """, {"cena":cena, "barva":barva, "moc_motorja":moc_motorja, "poraba":poraba})
    
        conn.execute(
            """
            INSERT INTO Znamka (ime) VALUES ('Hyundai')
            """
        )

        conn.execute(
            """INSERT INTO Znamka (ime) VALUES ('Alfa Romeo')""")
        

def pripravi_bazo(conn):
    '''Pripravimo bazo'''
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() != (0, ):
            return
    naredi_tabelo(conn)
    dodaj_podatke(conn)