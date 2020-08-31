# Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import uuid

# App

app = Flask(__name__)
CORS(app)

# sqlite setup
db = "flask/PekoInstallations.db"
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

@app.route("/nieuw/installatie", methods=['POST'])
def nieuwe_intallatie():
    with sqlite3.connect(db) as con:
        c = con.cursor()
        if request.method == 'GET':
            nieuwe_i = c.execute("INSERT INTO onderhoudsets VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",uuid.uuid4(), [request.form['klant'], request.form['adres'], request.form['type'], request.form['datum_installatie'],request.form['datum_installatie'], request.form['onderhoud_peko'], request.form['onderhoud_atag'], request.form['p_nummer'], request.form['dagen_tot_onderhoud']])
            return jsonify(nieuwe_i)




@app.route("/klanten", methods=['GET','POST'])
def klanten():
    try:
        with sqlite3.connect(db) as con:
            c = con.cursor()
            if request.method == 'GET':
                klanten_cursor = c.execute("select * FROM klanten")
                klanten = [{"id":k[0],"naam":k[1],"telefoon":k[2],"mail":k[3]} for k in klanten_cursor]
                return jsonify(klanten)

            elif request.method == 'POST':
                c.execute("INSERT INTO klanten VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), request.form['naam'], request.form['telefoon'], request.form['mail']))
                return jsonify(c.lastrowid)
    except Exception as e:
        print(e)

@app.route("/installaties", methods=['GET','POST'])
def instalaties():
    try:
        with sqlite3.connect(db) as con:
            c = con.cursor()
            if request.method == 'GET':
                installaties_cursor = c.execute("select * FROM installaties")
                instalaties = [{"id":k[0],"klant":k[1],"adres":k[2],"type":k[3],"datum_intallatie":k[4],"laatste_onderhoud":k[5],"onderhoud_peko":k[6],"onderhoude_atag":k[7],"p_nummer":k[8],"dagen_tot_onderhoud":k[9],"mail_verstuurd":k[10]} for k in installaties_cursor]
                return jsonify(instalaties)
            elif request.method == 'POST':
                c.execute("INSERT INTO onderhoudsets VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",uuid.uuid4(), [request.form['klant'], request.form['adres'], request.form['type'], request.form['datum_installatie'],request.form['datum_installatie'], request.form['onderhoud_peko'], request.form['onderhoud_atag'], request.form['p_nummer'], request.form['dagen_tot_onderhoud']])
                return jsonify(c.lastrowid)
    except Exception as e:
        print(e)

# Setup

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
