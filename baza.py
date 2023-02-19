import re
import requests
import cars

def naredi_tabelo(conn):
    '''USTVARIMO BAZO'''
    with conn:
        # POGON
        conn.execute(
            """CREATE TABLE IF NOT EXISTS pogon (id INTEGER PRIMARY KEY,
                tip_pogona TEXT)
            """),
        # GORIVO
        conn.execute(
            """CREATE TABLE IF NOT EXISTS gorivo (id INTEGER PRIMARY KEY,
                tip_goriva TEXT)
            """),
        # MENJALNIK
        conn.execute(
            """CREATE TABLE IF NOT EXISTS menjalnik (id INTEGER PRIMARY KEY,
                tip_menjalnika TEXT)
            """)
        # ZNAMKE
        conn.execute(
            """CREATE TABLE IF NOT EXISTS znamke (id INTEGER PRIMARY KEY,
                znamka TEXT)
            """),
        # MODELI
        conn.execute(
            """CREATE TABLE IF NOT EXISTS modeli(
                id INTEGER PRIMARY KEY,
                model TEXT,
                znamka_id INTEGER,
                url_naslov VARCHAR,
                FOREIGN KEY(znamka_id) REFERENCES znamke(id))
            """),
        # AVTO
        conn.execute(
            """CREATE TABLE IF NOT EXISTS avto(
                id INTEGER PRIMARY KEY,
                visina INTEGER,
                dolzina INTEGER,
                sirina INTEGER,
                tip_motorja VARCHAR,
                stevilo_prestav INTEGER,
                moc_motorja INTEGER,
                navor INTEGER,
                mestna_poraba INTEGER,
                avtocestna_poraba INTEGER,
                model_id INTEGER,
                menjalnik_id INTEGER,
                gorivo_id INTEGER,
                pogon_id INTEGER,
                FOREIGN KEY(model_id) REFERENCES modeli(id),
                FOREIGN KEY(menjalnik_id) REFERENCES menjalnik(id),
                FOREIGN KEY(gorivo_id) REFERENCES gorivo(id),
                FOREIGN KEY(pogon_id) REFERENCES pogon(id))
            """),
        # UPORABNIK
        conn.execute(
            """CREATE TABLE IF NOT EXISTS uporabnik (id INTEGER PRIMARY KEY,
                uporabniskoIme TEXT,
                geslo TEXT)
            """),
        # KOMENTAR
        conn.execute(
            """CREATE TABLE IF NOT EXISTS komentar (id INTEGER PRIMARY KEY,
                uporabnik TEXT,
                cas TIMESTAMP,
                opis TEXT,
                znamka TEXT,
                model TEXT
            """)

def pridobi_sliko(link):
    """PRIDOBI SLIKO S SPLETA"""
    html = requests.get(link).text
    regex_link = r"<source media=\"\(min-width:1280px\)\" srcset=\"([^\"]*)\">"
    slika = re.findall(regex_link, html)
    return slika[0] if slika != [] else None

seznam_avtomobilov = cars.get_car()

def dodaj_podatke(conn):
    '''DODAMO PODATKE V BAZO'''
    with conn:
        znamke = set()
        modeli = set()
        tipi_menjalnikov = set()
        tipi_pogonov = set()
        tipi_goriv = set()
        for avto in seznam_avtomobilov:
            # POGON
            pogon = avto["Engine Information"]["Driveline"].split()[0]
            if pogon not in tipi_pogonov:
                tipi_pogonov.add(pogon)
                conn.execute(
                """
                INSERT INTO pogon(tip_pogona) 
                VALUES (?)
                """,[pogon])
            # GORIVO
            gorivo = avto["Fuel Information"]["Fuel Type"]
            if gorivo not in tipi_goriv:
                tipi_goriv.add(gorivo)
                conn.execute(
                """
                INSERT INTO gorivo(tip_goriva) 
                VALUES (?)
                """,[gorivo])
            # MENJALNIK
            menjalnik = avto["Identification"]["Classification"].split()[0]
            if menjalnik not in tipi_menjalnikov:
                tipi_menjalnikov.add(menjalnik)
                conn.execute(
                """
                INSERT INTO menjalnik(tip_menjalnika) 
                VALUES (?)
                """,[menjalnik])
            # ZNAMKE
            znamka = avto["Identification"]["Make"]
            if znamka not in znamke:
                znamke.add(znamka)
                conn.execute(
                """
                INSERT INTO znamke(znamka) 
                VALUES (?)
                """,[znamka])
            # MODELI
            model = avto["Identification"]["ID"].split()[2]
            if model not in modeli:
                link = pridobi_sliko("https://www.autoblog.com/" + znamka.lower() + "/" + model.lower() + "/")
                modeli.add(model)
                conn.execute(
                """
                INSERT INTO modeli(model, znamka_id, url_naslov) 
                VALUES (?, (SELECT id FROM znamke WHERE znamka = ?), ?)
                """,[model, znamka, link])
            # AVTO
            visina = avto["Dimensions"]["Height"]
            dolzina = avto["Dimensions"]["Length"]
            sirina = avto["Dimensions"]["Width"]
            tip_motorja = avto["Engine Information"]["Engine Type"].split()[1]
            stevilo_prestav = avto["Engine Information"]["Number of Forward Gears"]
            moc_motorja = avto["Engine Information"]["Engine Statistics"]["Horsepower"] 
            navor = str(round(int(avto["Engine Information"]["Engine Statistics"]["Torque"]) * 1.3558)) # Pretvorba iz pound-foot v Nm
            mestna_poraba = str(round(int(avto["Fuel Information"]["City mpg"]) * 1.609344)) # Pretvorba iz mp/h v km/h
            avtocestna_poraba = str(round(int(avto["Fuel Information"]["Highway mpg"]) * 1.609344)) # Pretvorba iz mp/h v km/h
            conn.execute("""
                INSERT INTO avto(visina, dolzina, sirina, tip_motorja, stevilo_prestav, moc_motorja, navor, mestna_poraba, avtocestna_poraba, model_id, menjalnik_id, gorivo_id, pogon_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, (SELECT id FROM modeli WHERE model = ?), (SELECT id FROM menjalnik WHERE tip_menjalnika = ?), (SELECT id FROM gorivo WHERE tip_goriva = ?), (SELECT id FROM pogon WHERE tip_pogona = ?))
                """,[visina, dolzina, sirina, tip_motorja, stevilo_prestav, moc_motorja, navor, mestna_poraba, avtocestna_poraba, model, menjalnik, gorivo, pogon])

def pripravi_bazo(conn):
    '''Pripravimo bazo'''
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() != (0, ):
            return
    naredi_tabelo(conn)
    dodaj_podatke(conn)