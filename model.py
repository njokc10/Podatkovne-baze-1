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

class Gorivo:
    def __init__(self, id, tip_goriva):
        self.id = id
        self.tip_goriva = tip_goriva

    @staticmethod
    def dobi_vse_gorivo():
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

    @staticmethod
    def dobi_vse_menjalnik():
        with conn:
            cursor = conn.execute("""
                SELECT * FROM menjalnik
            """)
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

class Modeli:
    def __init__(self, id, model, znamka_id, url_naslov):
        self.id = id
        self.model = model
        self.znamka_id = znamka_id
        self.url_naslov = url_naslov

    @staticmethod
    def dobi_vse_modele():
        with conn:
            cursor = conn.execute("""
                SELECT * FROM modeli
            """)
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
    def dobi_avto_za_model(model):
        with conn:
            model_id = conn.execute('''SELECT id FROM modeli WHERE model=?''', [model])
            cursor = conn.execute("""
                SELECT * FROM Avto WHERE model_id=?
            """, [model_id])
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
    def __init__ (self, znamka, model, uporabnik, datum, ura, opis):
        self.znamka = znamka
        self.model = model
        self.uporabnik = uporabnik
        self.datum = datum
        self.ura = ura
        self.opis = opis

    # Vrni vse komentarje iz baze za doloceno znamko in model. Če oseba ni prijavljena vrni napako: 
    # "Oops! Prišlo je do napake. Pred oddajo komentarja se je potrebno prijaviti!"
    @staticmethod
    def dobi_komentarje(znamka, model):
        with conn:
            cursor = conn.execute("""
                SELECT * FROM komentar WHERE znamka=? AND model=?
            """, [znamka, model])
            podatki = list(cursor.fetchall())
            return [Komentar(pod[0], pod[1], pod[2], pod[3], pod[4], pod[5]) for pod in podatki]
        return []

    # Shrani komentar v bazo za doloceno znamko in model
    def shrani_komentar(self):
        '''Shrani komentar v bazo'''
        with conn:
            conn.execute("""
            INSERT INTO komentar (znamka, model, uporabnik, datum, ura, opis) VALUES (?,?,?,?,?,?)
            """, [self.znamka, self.model, self.uporabnik, self.datum, self.ura, self.opis])
    
    # Izbriši komentar iz baze za dolocen ID