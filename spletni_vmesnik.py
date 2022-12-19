import bottle
import model

glavni_model = model.Model()

@bottle.route("/static/img/<filename>")
def serve_static_file_img(filename):
    return bottle.static_file(filename, root="./static/img")

@bottle.route("/static/css/<filename>")
def serve_static_file_css(filename):
    return bottle.static_file(filename, root="./static/css")

# To je dekorator. Ko pridemo na mesto z naslovom "/" se pozene funkcija glavna_stran
@bottle.route("/")
def glavna_stran():
    podatki = glavni_model.dobi_vse_uporabnike()
    return bottle.template("glavna.html", uporabniki=podatki)

bottle.run(debug=True, reloader=True)