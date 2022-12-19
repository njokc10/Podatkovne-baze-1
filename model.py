# Model bo delal vse kar je povezano z bazo
# Samo tukaj se pogovarjamo z bazo

import sqlite3
import baza

conn = sqlite3.connect("baza.sqlite3")

#TODO Ustvarimo bazo

baza.pripravi_vse(conn)

class Model:
    def dobi_vse_uporabnike(self):
        with conn:
            cur = conn.execute("""
                SELECT * FROM uporabnik
            """)

            return cur.fetchall()