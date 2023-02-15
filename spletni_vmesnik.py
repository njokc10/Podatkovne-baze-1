import bottle
import model
import hashlib

glavni_model = model.Model()

def geslo_md5(s):
    '''Vrne MD5 hash danega UTF-8 niza.'''
    # Geslo zakodiramo, preden ga spravimo v bazo
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

secret = 'skrivnost'

@bottle.route("/")
def glavna_stran():
    '''Vrne glavno stran'''
    podatki = glavni_model.dobi_vse_avte()
    return bottle.template("glavna.html", avtomobili=podatki)

@bottle.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./static/img')

@bottle.route("/prijava")
def prijava():
    '''Vrne stran za prijavo'''
    return bottle.template('prijava.html')

@bottle.post('/prijava')
def prijava_post():
    '''Obdelaj izpolnjeno formo za prijavo'''
    # Uporabniško ime
    uporabnisko_ime = bottle.request.forms.uname
    # Geslo (zakodiramo)
    geslo = geslo_md5(bottle.request.forms.psw)
    # Preverimo, ali se je uporabnik pravilno prijavil
    poizvedba = model.Uporabnik.pravilen_vnos(uporabnisko_ime, geslo)
    if poizvedba is None:
        # Uporabnisko ime in geslo se ne ujemata
        print('Uporabnik ni najden')
        #return bottle.template('prijava.html', napaka='Uporabnik ne obstaja.')
    else:
        # Uporabnisko ime in geslo se ujemata
        print('Uporabnik najden!')
        #bottle.response.set_cookie('uporabniskoIme', uporabniskoIme, path='/', secret=secret)
        bottle.redirect('/')

@bottle.route("/registracija")
def registracija():
    '''Vrne stran za registracijo'''
    return bottle.template('registracija.html')

@bottle.post('/registracija')
def registracija_post():
    '''Registrira novega uporabnika.'''
    # Uporabnisko ime
    uporabnisko_ime = bottle.request.forms.uime
    # Geslo
    geslo1 = bottle.request.forms.psw
    geslo2 = bottle.request.forms.psw_repeat
    # Pogledamo, ce je uporabnik ze v bazi
    ui_poizvedba = model.Uporabnik.dobi_uporabnika(uporabnisko_ime)
    if ui_poizvedba:
        # print('Uporabnisko ime ze obstaja')
        # Uporabnisko ime ze obstaja
        return bottle.template('registracija.html', uporabniskoIme=uporabnisko_ime, napaka='Uporabnisko ime ze obstaja.')
    elif not geslo1 == geslo2:
        # Nepravilen vnos gesla pri registraciji
        return bottle.template('registracija.html', uporabniskoIme=uporabnisko_ime, napaka='Nepravilen vnos gesla')
    else:
        # Vstavimo novega uporabnika v bazo
        # print('ustvarjamo novega uporabnika')
        geslo = geslo_md5(geslo1)
        model.Uporabnik(uporabnisko_ime, geslo).shrani_v_bazo()
        bottle.response.set_cookie('uporabniskoIme', uporabnisko_ime, path='/', secret=secret)
        bottle.redirect('/')

# Pozenemo bottle
bottle.run(debug=True, reloader=True)