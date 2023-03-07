import bottle
import model
import hashlib
from datetime import date

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
    goriva = model.Gorivo.dobi_vse_gorivo()
    menjalniki = model.Menjalnik.dobi_vse_menjalnik()

    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)

    return bottle.template("glavna.html", znamke=znamke, modeli=modeli, goriva=goriva, menjalniki=menjalniki, trenutni_uporabnik=trenutni_uporabnik, _znamka=0, _model=0, _gorivo=0, _menjalnik=0)

@bottle.post("/")
def glavna_stran_post():
    '''Obdelaj izpolnjeno formo za iskanje vozila'''
    znamka = bottle.request.forms.znamka
    model_ = bottle.request.forms.model
    gorivo = bottle.request.forms.gorivo
    menjalnik = bottle.request.forms.menjalnik
    znamke = model.Znamke.dobi_vse_znamke()
    modeli = model.Modeli.dobi_vse_modele(znamka)
    goriva = model.Gorivo.dobi_vse_gorivo(model_)
    menjalniki = model.Menjalnik.dobi_vse_menjalnik(model_, gorivo)

    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)

    if znamka: 
        _znamka = znamka #shranimo znamko preden se osveži
    else:
        _znamka = 0 #ni bila izbrana nobena znamka

    if model_:
        _model = model_
    else:
        _model = 0

    if menjalnik:
        _menjalnik = menjalnik
    else:
        _menjalnik = 0

    if gorivo:
        _gorivo = gorivo
    else:
        _gorivo = 0

    if not (znamka and model_ and gorivo and menjalnik):
        return bottle.template("glavna.html", znamke=znamke, modeli=modeli, goriva=goriva, menjalniki=menjalniki, _znamka=_znamka, _model=_model, trenutni_uporabnik=trenutni_uporabnik, _gorivo=_gorivo, _menjalnik=_menjalnik)
    # Napisi poizvedbe in poslji na stran specifikacije
    model_url_naslov = model.Modeli.dobi_podatke_za_model(model_)
    podatki_avto = model.Avto.dobi_avto_za_model(model_, gorivo, menjalnik)
    # Filtriramo podatke avtomobila
    pravi_podatki_avto = filter(podatki_avto)
    # najde pogon glede na dane id-je pogona
    ids = [a.pogon_id for a in pravi_podatki_avto]
    pogoni = [model.Pogon.dobi_pogon(elt) for elt in ids]
    # najde znamko glede na dane id-je znamke
    znamka_ime = model.Znamke.dobi_znamko(znamka)
    return bottle.template('specifikacije.html', znamka=znamka_ime, model_=model_, gorivo=gorivo, menjalnik=menjalnik, model_url_naslov=model_url_naslov, podatki_avto=pravi_podatki_avto, pogoni=pogoni, trenutni_uporabnik=trenutni_uporabnik)

@bottle.route("/mnenja")
def mnenja_stran():
    '''Vrne stran mnenja'''
    znamke = model.Znamke.dobi_vse_znamke()
    modeli = model.Modeli.dobi_vse_modele()

    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)

    return bottle.template("mnenja.html", znamke=znamke, modeli=modeli, _znamka=0, trenutni_uporabnik=trenutni_uporabnik)

@bottle.post("/mnenja")
def mnenja_stran_post():
    '''Obdelaj izpolnjeno formo za oddajo komentarja'''
    znamka = bottle.request.forms.znamka
    model_ = bottle.request.forms.model
    znamke = model.Znamke.dobi_vse_znamke()
    modeli = model.Modeli.dobi_vse_modele(znamka)

    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)

    if znamka: 
        _znamka = znamka #shranimo znamko preden se osveži
    else:
        _znamka = 0 #ni bila izbrana nobena znamka
    if not (znamka and model_):
        return bottle.template("mnenja.html", znamke=znamke, modeli=modeli, _znamka=_znamka, trenutni_uporabnik=trenutni_uporabnik)
    # Napisi poizvedbe in poslji na stran komentar
    # najde znamko glede na dane id-je znamke
    znamka_ime = model.Znamke.dobi_znamko(znamka)
    komentarji = reversed(model.Komentar.dobi_vse_komentarje(model_))
    return bottle.template("komentar.html", znamke=znamka_ime, modeli=model_, trenutni_uporabnik=trenutni_uporabnik, komentarji=komentarji)

@bottle.post("/komentar")
def shrani_komentar():
    '''Vrne stran primerjava'''
    # opis
    text = bottle.request.forms.komentar
    model_ = bottle.request.forms.model

    # uporabnik
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if trenutni_uporabnik:
        # cas
        trenuten_datum = date.today()
        # Shrani v bazo
        model.Komentar(trenutni_uporabnik, trenuten_datum, text, model_).shrani_komentar()
    
    # komentarji = model.Komentar.dobi_vse_komentarje(model_)
    bottle.redirect("/mnenja")

@bottle.route("/primerjaj")   
def stran_primerjava():
    znamke = model.Znamke.dobi_vse_znamke()
    modeli = model.Modeli.dobi_vse_modele()
    gorivo = model.Gorivo.dobi_vse_gorivo()
    menjalnik = model.Menjalnik.dobi_vse_menjalnik()
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    return bottle.template("primerjava.html", znamke=znamke, _modeli_0=modeli, _modeli_1=modeli, gorivo=gorivo, menjalnik=menjalnik, _znamka_0=0, _znamka_1=0, trenutni_uporabnik=trenutni_uporabnik)

@bottle.post("/primerjaj")
def stran_primerjava_post():
    znamka_0 = bottle.request.forms.znamka_0
    model_0 = bottle.request.forms.model_0
    gorivo_0 = bottle.request.forms.gorivo_0
    menjalnik_0 = bottle.request.forms.menjalnik_0
    znamka_1 = bottle.request.forms.znamka_1
    model_1 = bottle.request.forms.model_1
    gorivo_1 = bottle.request.forms.gorivo_1
    menjalnik_1 = bottle.request.forms.menjalnik_1
    znamke = model.Znamke.dobi_vse_znamke()
    _modeli_0 = model.Modeli.dobi_vse_modele(znamka_0)
    _modeli_1 = model.Modeli.dobi_vse_modele(znamka_1)
    gorivo = model.Gorivo.dobi_vse_gorivo()
    menjalnik = model.Menjalnik.dobi_vse_menjalnik()
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if znamka_0: 
        _znamka_0 = znamka_0 #shranimo znamko preden se osveži
        if znamka_1:
            _znamka_1 = znamka_1 #shranimo drugo znamko preden se osveži
        else:
            _znamka_1 = 0 #ni bila izbrana druga znamka
    else:
        _znamka_0 = 0 #ni bila izbrana nobena znamka
        _znamka_1 = 0 #ni bila izbrana druga znamka
    if not (znamka_0 and model_0 and gorivo_0 and gorivo_0):
        return bottle.template("primerjava.html", znamke=znamke, _modeli_0=_modeli_0, _modeli_1=_modeli_1, gorivo=gorivo, menjalnik=menjalnik, _znamka_0=_znamka_0, _znamka_1=_znamka_1, trenutni_uporabnik=trenutni_uporabnik)
    if not (znamka_1 and model_1):
        return bottle.template("primerjava.html", znamke=znamke, _modeli_0=_modeli_0, _modeli_1=_modeli_1, gorivo=gorivo, menjalnik=menjalnik, _znamka_0=_znamka_0, _znamka_1=_znamka_1, trenutni_uporabnik=trenutni_uporabnik)
    # Napisi poizvedbe in poslji na stran specifikacije
    model_url_naslov_0 = model.Modeli.dobi_podatke_za_model(model_0)
    model_url_naslov_1 = model.Modeli.dobi_podatke_za_model(model_1)
    podatki_avto_0 = model.Avto.dobi_avto_za_model(model_0, gorivo_0, menjalnik_0)
    podatki_avto_1 = model.Avto.dobi_avto_za_model(model_1, gorivo_1, menjalnik_1)
    pravi_podatki_avto_0 = filter(podatki_avto_0)
    pravi_podatki_avto_1 = filter(podatki_avto_1)
    # najde pogon glede na dane id-je pogona
    ids_0 = [a.pogon_id for a in pravi_podatki_avto_0]
    pogoni_0 = [model.Pogon.dobi_pogon(elt) for elt in ids_0]
    ids_1 = [a.pogon_id for a in pravi_podatki_avto_1]
    pogoni_1 = [model.Pogon.dobi_pogon(elt) for elt in ids_1]
    # najde znamko glede na dane id-je znamke
    znamka_ime_0 = model.Znamke.dobi_znamko(znamka_0)
    znamka_ime_1 = model.Znamke.dobi_znamko(znamka_1)
    return bottle.template("prikazPrimerjaj.html", znamka_0 = znamka_ime_0, znamka_1 = znamka_ime_1, model_0 = model_0, model_1=model_1, gorivo_0=gorivo_0, gorivo_1=gorivo_1, menjalnik_0 = menjalnik_0, menjalnik_1=menjalnik_1, model_url_naslov_0=model_url_naslov_0, model_url_naslov_1=model_url_naslov_1, podatki_avto_0=pravi_podatki_avto_0,podatki_avto_1=pravi_podatki_avto_1, pogoni_0=pogoni_0, pogoni_1=pogoni_1, trenutni_uporabnik=trenutni_uporabnik)

@bottle.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./static/img')

@bottle.route("/prijava")
def prijava():
    '''Vrne stran za prijavo'''
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    return bottle.template('prijava.html', napaka=None, trenutni_uporabnik=trenutni_uporabnik)

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
        trenutni_uporabnik = None
        return bottle.template('prijava.html', napaka='Uporabnik ne obstaja!', trenutni_uporabnik=trenutni_uporabnik)
    else:
        # Uporabnisko ime in geslo se ujemata, uporabnik je prijavljen
        bottle.response.set_cookie('uporabniskoIme', uporabnisko_ime, path='/', secret=secret)
        bottle.redirect('/')

@bottle.route('/odjava')
def logout():
   '''
   Pobrisi piškotke
   '''
   bottle.response.delete_cookie('uporabniskoIme')
   bottle.redirect('/')

@bottle.route("/registracija")
def registracija():
    '''Vrne stran za registracijo'''
    return bottle.template('registracija.html', napaka=None, trenutni_uporabnik=None)

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
        return bottle.template('registracija.html', napaka='To uporabnisko ime ze obstaja!', trenutni_uporabnik=None)
    elif not geslo1 == geslo2:
        # Nepravilen vnos gesla pri registraciji
        return bottle.template('registracija.html', napaka='Nepravilen vnos gesla!', trenutni_uporabnik=None)
    else:
        # Vstavimo novega uporabnika v bazo
        geslo = geslo_md5(geslo1)
        model.Uporabnik(uporabnisko_ime, geslo).shrani_v_bazo()
        bottle.response.set_cookie('uporabniskoIme', uporabnisko_ime, path='/', secret=secret)
        bottle.redirect('/')

def filter(cars_specs):
    '''Vrne filtrirane podatke avtomobila'''
    # Hranimo ze najdene specifikacije
    d = {'moc_motorja': set(),
         'navor': set(),
         'tip_motorja': set()}

    _cars_specs = []
    for car in cars_specs:
        if not(car.moc_motorja in d['moc_motorja'] and car.navor in d['navor'] and car.tip_motorja in d['tip_motorja']):
            _cars_specs.append(car)
            d['moc_motorja'].add(car.moc_motorja)
            d['navor'].add(car.navor)
            d['tip_motorja'].add(car.tip_motorja)
    return _cars_specs[:3]

# Pozenemo bottle
bottle.run(debug=True, reloader=True)