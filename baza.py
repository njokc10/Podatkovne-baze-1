def naredi_tabelo(conn):
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS 
            uporabnik (
                uid INTEGER PRIMARY KEY,
                username TEXT,
                name TEXT
            )
            """
        )

def dodaj_podatke(conn):
    with conn:
        conn.execute("""
        INSERT INTO uporabnik 
        (username, name) VALUES
        ("email@email.com", "Neko ime")
        """)

def pripravi_bazo(conn):
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() != (0, ):
            return
    naredi_tabelo(conn)
    dodaj_podatke(conn)