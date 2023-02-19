import bottle
import model
import hashlib

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
    znamke = model.Znamke.dobi_vse_znamke()
    modeli = model.Modeli.dobi_vse_modele()
    gorivo = model.Gorivo.dobi_vse_gorivo()
    menjalnik = model.Menjalnik.dobi_vse_menjalnik()
    return bottle.template("glavna.html", znamke=znamke, modeli=modeli, gorivo=gorivo, menjalnik=menjalnik)

@bottle.post("/")
def glavna_stran_post():
    '''Obdelaj izpolnjeno formo za iskanje vozila'''
    znamka = bottle.request.forms.znamka
    model_ = bottle.request.forms.model
    gorivo = bottle.request.forms.gorivo
    menjalnik = bottle.request.forms.menjalnik
    # Napisi poizvedbe in poslji na stran specifikacije
    model_url_naslov = model.Modeli.dobi_podatke_za_model(model_)
    return bottle.template('specifikacije.html', znamka=znamka, model_=model_, gorivo=gorivo, menjalnik=menjalnik, model_url_naslov=model_url_naslov)

@bottle.route("/mnenja")
def mnenja_stran():
    '''Vrne stran mnenja'''
    znamke = model.Znamke.dobi_vse_znamke()
    modeli = model.Modeli.dobi_vse_modele()
    return bottle.template("mnenja.html", znamke=znamke, modeli=modeli)

@bottle.route("/primerjava")
def mnenja_stran():
    '''Vrne stran primerjava'''
    return bottle.template("primerjava.html")

@bottle.route("/specifikacije")
def mnenja_stran():
    '''Vrne stran specifikacije'''
    return bottle.template("specifikacije.html")

#@bottle.post('/specifikacije')
#def specifikacije_post():
#    '''Obdelaj izpolnjeno formo za prijavo'''
#    # Uporabniško ime
#    uporabnisko_ime = bottle.request.forms.uname
#    # Geslo (zakodiramo)
#    geslo = geslo_md5(bottle.request.forms.psw)
#    # Preverimo, ali se je uporabnik pravilno prijavil
#    poizvedba = model.Uporabnik.pravilen_vnos(uporabnisko_ime, geslo)
#    if poizvedba is None:
#        # Uporabnisko ime in geslo se ne ujemata
#        return bottle.template('prijava.html', napaka='Uporabnik ne obstaja!')
#    else:
#        bottle.redirect('/specifikacije')

@bottle.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./static/img')

@bottle.route("/prijava")
def prijava():
    '''Vrne stran za prijavo'''
    return bottle.template('prijava.html', napaka=None)

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
        return bottle.template('prijava.html', napaka='Uporabnik ne obstaja!')
    else:
        # Uporabnisko ime in geslo se ujemata, uporabnik je prijavljen
        bottle.response.set_cookie('uporabniskoIme', uporabnisko_ime, path='/', secret=secret)
        bottle.redirect('/')

#@bottle.route('/logout')
#def logout():
#    '''
#    Pobrisi piškotke
#    '''
#    bottle.response.delete_cookie('uporabniskoIme')
#    bottle.redirect('/')

@bottle.route("/registracija")
def registracija():
    '''Vrne stran za registracijo'''
    return bottle.template('registracija.html', napaka=None)

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
        # Uporabnisko ime ze obstaja
        return bottle.template('registracija.html', napaka='To uporabnisko ime ze obstaja!')
    elif not geslo1 == geslo2:
        # Nepravilen vnos gesla pri registraciji
        return bottle.template('registracija.html', napaka='Nepravilen vnos gesla!')
    else:
        # Vstavimo novega uporabnika v bazo
        geslo = geslo_md5(geslo1)
        model.Uporabnik(uporabnisko_ime, geslo).shrani_v_bazo()
        bottle.response.set_cookie('uporabniskoIme', uporabnisko_ime, path='/', secret=secret)
        bottle.redirect('/')

# Pozenemo bottle
bottle.run(debug=True, reloader=True)