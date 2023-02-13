# Model bo delal vse kar je povezano z bazo
# Samo tukaj se pogovarjamo z bazo

import sqlite3
import baza

conn = sqlite3.connect("baza.sqlite3")

#TODO Ustvarimo bazo

baza.pripravi_bazo(conn)

class Model:
    def dobi_vse_avte(self):
        with conn:
            cur = conn.execute("""
                SELECT * FROM Avto
            """)
            return cur.fetchall()