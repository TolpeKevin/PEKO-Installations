# Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

# App

app = Flask(__name__)
CORS(app)

# sqlite setup
db = "PekoInstallations.db"
try:
    f = open(db)
except FileNotFoundError:
    print("No database found")
else:
    print("Database found")
    f.close()

# Routes

@app.route("/")
def init():
    return jsonify('Initializing')

@app.route("/nieuw/klant")
def nieuwe_klant():
    with sqlite3.connect(db) as con:
            c = con.cursor()
            nieuwe_klant = c.execute("INSERT INTO klanten VALUES (%s, %s, %s, %s)", [request.form['klant'], request.form['naam'], request.form['telefoon'], request.form['mail']])


            nieuwe_klant = c.execute("INSERT INTO klanten VALUES (%s, %s, %s, %s, %s, %s, %s)", [request.form['klant'], request.form['adres'], request.form['type'], request.form['datum_installatie'],request.form['onderhoud_peko'], request.form['onderhoud_atag'], request.form['p_nummer']])
    return jsonify(nieuwe_klant)

@app.route("/klanten")
def klanten():
    with sqlite3.connect(db) as con:
        c = con.cursor()
        klanten_cursor = c.execute("select * FROM klanten")
        klanten = [{"id":k[0],"naam":k[1],"adres":k[2],"type":k[3],"datum_installatie":k[4],"onderhoud_peko":k[5],"onderhoud_atag":k[6],"p_nummer":k[1]} for k in klanten_cursor]
    return jsonify(klanten)

@app.route("/verwijder")
def verwijder():
    pass

@app.route("/update")
def update():
    klant = c.execute("UPDATE klanten set klant = %s, adres = %s, type = %s, datum_installatie= %s, onderhoud_peko = %s, onderhoud_atag = %s, p_nummer = %s)", [request.form['klant'], request.form['adres'], request.form['type'], request.form['datum_installatie'],request.form['onderhoud_peko'], request.form['onderhoud_atag'], request.form['p_nummer']])
    return jsonify(klant)

# Setup

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
