# Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import uuid, time, datetime

# App

app = Flask(__name__)
CORS(app)

# sqlite setup
db = "./PekoInstallations.db"
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
                c.execute("INSERT INTO klanten VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), request.json['naam'], request.json['telefoon'], request.json['mail']))
                return jsonify(c.lastrowid)
    except Exception as e:
        print(e)

@app.route("/installaties", methods=['GET','POST'])
def installaties():
    try:
        with sqlite3.connect(db) as con:
            c = con.cursor()
            if request.method == 'GET':
                installaties_cursor = c.execute("select * FROM installaties")
                installaties_dict = [{"id":k[0],"klant":k[1],"adres":k[2],"type":k[3],"datum_intallatie":k[4],"laatste_onderhoud":k[5],"onderhoud_peko":k[6],"onderhoude_atag":k[7],"p_nummer":k[8],"dagen_tot_onderhoud":k[9],"mail_verstuurd":k[10]} for k in installaties_cursor]
                return jsonify(installaties_dict)
            elif request.method == 'POST':
                print("->",request.json.get('dagen_tot_onderhoud'))
                c.execute("INSERT INTO installaties VALUES (?,?,?,?,?,?,?,?,?,?,?)",(str(uuid.uuid4()), request.json.get('klant'), request.json.get('adres'), request.json.get('type') ,request.json.get('datum_installatie') if request.json.get('datum_installatie') != '' else time.mktime(datetime.date.today().timetuple()),request.json.get('datum_installatie') if request.json.get('laatste_onderhoud') != '' else time.mktime(datetime.date.today().timetuple()), request.json.get('onderhoud_peko'), request.json.get('onderhoud_atag'), request.json.get('p_nummer'), request.json.get('dagen_tot_onderhoud'), request.json.get('mail_verstuurd')))
                return jsonify(c.lastrowid)
    except Exception as e:
        print(e)

# Setup

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
