# Model bo delal vse kar je povezano z bazo
# Samo tukaj se pogovarjamo z bazo

import sqlite3
import baza

# Povezava do baze
conn = sqlite3.connect("baza.sqlite3")

# Pripravimo bazo
baza.pripravi_bazo(conn)

class Model:
    def dobi_vse_avte(self):
        with conn:
            cur = conn.execute("""
                SELECT * FROM Avto
            """)
            return cur.fetchall()

    def dobi_vse_znamke(self):
        with conn:
            cur = conn.execute("""
            SELECT ime FROM Znamka
            """)
            return cur.fetchall()
    
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
                WHERE uporabniskoIme=? AND geslo=?
            """, [uporabniskoIme, geslo])
            if cursor.fetchone():
                return cursor
            return None

   
