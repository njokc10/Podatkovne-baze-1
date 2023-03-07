# Model bo delal vse kar je povezano z bazo
# Samo tukaj se pogovarjamo z bazo

import sqlite3
import baza

# Povezava do baze
conn = sqlite3.connect("baza.sqlite3")

# Pripravimo bazo
baza.pripravi_bazo(conn)

class Pogon:
    def __init__(self, id, tip_pogona):
        self.id = id
        self.tip_pogona = tip_pogona

    # Vrne id in tip pogona glede na podani id
    @staticmethod
    def dobi_pogon(id_pogon):
        with conn:
            cursor = conn.execute("""
                SELECT * FROM pogon WHERE pogon.id = ?
            """, [id_pogon])
            podatki = list(cursor.fetchall())
            return [Pogon(pod[0], pod[1]) for pod in podatki]
        return []

class Gorivo:
    def __init__(self, id, tip_goriva):
        self.id = id
        self.tip_goriva = tip_goriva

    # Vrne vse vrste goriva
    @staticmethod
    def dobi_vse_gorivo(model=None):
        if model:
            with conn:
                cursor = conn.execute("""
                    SELECT DISTINCT gorivo_id, tip_goriva FROM avto INNER JOIN modeli on (avto.model_id=modeli.id) 
                    INNER JOIN gorivo on (avto.gorivo_id=gorivo.id) WHERE model = ?
                """, [model])
                podatki = list(cursor.fetchall())
                return [Gorivo(pod[0], pod[1]) for pod in podatki]
        else:
            with conn:
                cursor = conn.execute("""
                    SELECT * FROM gorivo 
                """)
                podatki = list(cursor.fetchall())
                return [Gorivo(pod[0], pod[1]) for pod in podatki]
        return []

class Menjalnik:
    def __init__(self, id, tip_menjalnika):
        self.id = id
        self.tip_menjalnika = tip_menjalnika

    # Vrne vse vrste menjalnikov
    @staticmethod
    def dobi_vse_menjalnik(model=None, gorivo=None):
        if not (model and gorivo):
            with conn:
                cursor = conn.execute("""
                    SELECT * FROM menjalnik
                """)
                podatki = list(cursor.fetchall())
                return [Menjalnik(pod[0], pod[1]) for pod in podatki]
        else:
            with conn:
                cursor = conn.execute("""
                    SELECT DISTINCT menjalnik_id, tip_menjalnika FROM avto INNER JOIN modeli on (avto.model_id=modeli.id) 
                    INNER JOIN gorivo on (avto.gorivo_id=gorivo.id) INNER JOIN menjalnik on (avto.menjalnik_id = menjalnik.id) 
                    WHERE model = ? AND tip_goriva = ?
                """, [model, gorivo])
                podatki = list(cursor.fetchall())
                return [Menjalnik(pod[0], pod[1]) for pod in podatki]
        return []

class Znamke:
    def __init__(self, id, znamka):
        self.id = id
        self.znamka = znamka

    @staticmethod
    def dobi_vse_znamke():
        with conn:
            cursor = conn.execute("""
                SELECT * FROM znamke
            """)
            podatki = list(cursor.fetchall())
            return [Znamke(pod[0], pod[1]) for pod in podatki]
        return []

    @staticmethod
    def dobi_znamko(id_znamka):
        with conn:
            cursor = conn.execute("""
                SELECT * FROM znamke WHERE znamke.id = ?
            """, [id_znamka])
            podatki = list(cursor.fetchall())
            return [Znamke(pod[0], pod[1]) for pod in podatki]
        return []

class Modeli:
    def __init__(self, id, model, znamka_id , url_naslov):
        self.id = id
        self.model = model
        self.znamka_id = znamka_id
        self.url_naslov = url_naslov

    @staticmethod
    def dobi_vse_modele(znamka = None):
        if znamka:
            with conn:
                cursor = conn.execute("""
                    SELECT * FROM modeli WHERE znamka_id = ?
                """, [znamka])
                podatki = list(cursor.fetchall())
                return [Modeli(pod[0], pod[1], pod[2], pod[3]) for pod in podatki]
        return []
        
    @staticmethod
    def dobi_podatke_za_model(model):
        with conn:
            cursor = conn.execute("""
                SELECT * FROM modeli WHERE model=?
            """, [model])
            podatki = list(cursor.fetchall())
            return [Modeli(pod[0], pod[1], pod[2], pod[3]) for pod in podatki]
        return []

class Avto:
    def __init__(self, id, visina, dolzina, sirina, tip_motorja, stevilo_prestav, moc_motorja, navor, mestna_poraba, avtocestna_poraba, model_id, menjalnik_id, gorivo_id, pogon_id):
        self.id = id
        self.visina = visina
        self.dolzina = dolzina
        self.sirina = sirina
        self.tip_motorja = tip_motorja
        self.stevilo_prestav = stevilo_prestav
        self.moc_motorja = moc_motorja
        self.navor = navor
        self.mestna_poraba = mestna_poraba
        self.avtocestna_poraba = avtocestna_poraba
        self.model_id = model_id
        self.menjalnik_id = menjalnik_id
        self.gorivo_id = gorivo_id
        self.pogon_id = pogon_id

    @staticmethod
    def dobi_avte():
        with conn:
            cursor = conn.execute("""
                SELECT * FROM Avto
            """)
            podatki = list(cursor.fetchall())
            return [Avto(pod[0], pod[1], pod[2], pod[3], pod[4], pod[5], pod[6], pod[7], pod[8], pod[9], pod[10], pod[11], pod[12], pod[13]) for pod in podatki]
        return []
    
    @staticmethod
    def dobi_avto_za_model(model, gorivo, menjalnik):
        with conn:
            model_i = conn.execute("""SELECT id FROM modeli WHERE model=?""", [model])
            podatki1 = list(model_i.fetchall())
            model_id = [elt[0] for elt in podatki1]
            gorivo_i = conn.execute("""SELECT id FROM gorivo WHERE tip_goriva=?""", [gorivo])
            podatki2 = list(gorivo_i.fetchall())
            gorivo_id = [elt[0] for elt in podatki2]
            menjalnik_i = conn.execute("""SELECT id FROM menjalnik WHERE tip_menjalnika=?""", [menjalnik])
            podatki3 = list(menjalnik_i.fetchall())
            menjalnik_id = [elt[0] for elt in podatki3]
            cursor = conn.execute("""SELECT * FROM avto WHERE (model_id=? AND menjalnik_id=? AND gorivo_id=?);""", [model_id[0], gorivo_id[0], menjalnik_id[0]])
            podatki = list(cursor.fetchall())
            return [Avto(pod[0], pod[1], pod[2], pod[3], pod[4], pod[5], pod[6], pod[7], pod[8], pod[9], pod[10], pod[11], pod[12], pod[13]) for pod in podatki]
        return []

class Uporabnik:
    def __init__(self, uporabniskoIme=None, geslo=None):
        self.uporabniskoIme = uporabniskoIme
        self.geslo = geslo

    def __str__(self):
        return self.uporabniskoIme

    def shrani_v_bazo(self):
        '''
        Shrani uporabnika v bazo
        '''
        with conn:
            conn.execute('''
            INSERT INTO uporabnik (uporabniskoIme, geslo) VALUES (?,?)
            ''', [self.uporabniskoIme, self.geslo])

    @staticmethod
    def dobi_uporabnika(uporabniskoIme):
        with conn:
            cursor = conn.execute("""
                SELECT uporabniskoIme, geslo 
                FROM uporabnik
                WHERE uporabniskoIme=?
            """, [uporabniskoIme])
            if cursor.fetchone():
                return cursor
            return None

    @staticmethod
    def pravilen_vnos(uporabniskoIme, geslo):
        with conn:
            cursor = conn.execute("""
                SELECT uporabniskoIme, geslo 
                FROM uporabnik
                WHERE uporabniskoIme=? AND geslo=?;
            """, [uporabniskoIme, geslo])
            if cursor.fetchone():
                return cursor
            return None
        
class Komentar:
    def __init__ (self, uporabnik, cas, opis, model):
        self.uporabnik = uporabnik
        self.cas = cas
        self.opis = opis
        self.model = model

    # Vrni vse komentarje iz baze za doloceno znamko in model. Če oseba ni prijavljena vrni napako: 
    # "Oops! Prišlo je do napake. Pred oddajo komentarja se je potrebno prijaviti!"
    @staticmethod
    def dobi_vse_komentarje(model):
        with conn:
            cursor = conn.execute("""
                SELECT * FROM komentar WHERE model=?
            """, [model])
            podatki = list(cursor.fetchall())
            return [Komentar(pod[1], pod[2], pod[3], pod[4]) for pod in podatki]
        return []

    # Shrani komentar v bazo za doloceno model
    def shrani_komentar(self):
        '''Shrani komentar v bazo'''
        with conn:
            conn.execute("""
            INSERT INTO komentar (uporabnik, cas, opis, model) VALUES (?,?,?,?)
            """, [self.uporabnik, self.cas, self.opis, self.model])