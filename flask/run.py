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
    conn = sqlite3.connect(db)
    c = conn.cursor()

# Routes

@app.route("/")
def init():
    return jsonify('Initializing')

@app.route("/nieuw")
def nieuw():
    nieuwe_klant = c.execute("INSERT INTO klanten VALUES (%s, %s, %s, %s, %s, %s, %s)", [request.form['klant'], request.form['adres'], request.form['type'], request.form['datum_installatie'],request.form['onderhoud_peko'], request.form['onderhoud_atag'], request.form['p_nummer']])
    return jsonify(nieuwe_klant)

@app.route("/klanten")
def klanten():
    klanten = c.execute("select * FROM klanten")
    return jsonify(klanten)

# Setup

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
