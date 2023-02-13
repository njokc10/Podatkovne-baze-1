import bottle
import model

glavni_model = model.Model()

#def password_md5(s):
#    '''
#    Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
#    kodirana s to funkcijo.
#    '''
#    h = hashlib.md5()
#    h.update(s.encode('utf-8'))
#    return h.hexdigest()

# To je dekorator. Ko pridemo na mesto z naslovom "/" se pozene funkcija glavna_stran
@bottle.route("/")
def glavna_stran():
    podatki = glavni_model.dobi_vse_avte()
    return bottle.template("glavna.html", avtomobili=podatki)

@bottle.route("/prijava")
def prijava():
    return bottle.template('prijava.html')

@bottle.route("/registracija")
def registracija():
    return bottle.template('registracija.html')

# Pozenemo spletni
bottle.run(debug=True, reloader=True)