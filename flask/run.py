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
                c.execute("INSERT INTO klanten VALUES (?, ?, ?, ?)",[str(uuid.uuid4()), request.json['naam'], request.json['telefoon'], request.json['mail']])
                return jsonify(c.lastrowid)

            elif request.method == 'PUT':
                c.execute("update klanten set naam = ?, telefoon = ?, mail = ? where id = ?", [request.json['naam'], request.json['telefoon'], request.json['mail'], request.json['id']])
                return jsonify({"message":"succes"})

    except Exception as e:
        print(e)

@app.route("/installaties", methods=['GET','POST','PUT'])
def installaties():
    try:
        with sqlite3.connect(db) as con:
            c = con.cursor()
            if request.method == 'GET':
                c.execute("select * FROM installaties")
                installaties_dict = [{"id":k[0],"klant":k[1],"adres":k[2],"type":k[3],"datum_intallatie":k[4],"laatste_onderhoud":k[5],"onderhoud_peko":k[6],"onderhoude_atag":k[7],"p_nummer":k[8],"dagen_tot_onderhoud":k[9],"mail_verstuurd":k[10]} for k in c.fetchall()]
                return jsonify(installaties_dict)

            elif request.method == 'POST':
                nieuwe_installatie = valideer_installatie_request(request, "POST")
                if nieuwe_installatie:
                    c.execute("INSERT INTO installaties VALUES (?,?,?,?,?,?,?,?,?,?,?)",(str(uuid.uuid4()), nieuwe_installatie['klant'], nieuwe_installatie['adres'], nieuwe_installatie['type'] ,nieuwe_installatie['datum_installatie'],nieuwe_installatie['datum_installatie'], nieuwe_installatie['onderhoud_peko'], nieuwe_installatie['onderhoud_atag'], nieuwe_installatie['p_nummer'], nieuwe_installatie['dagen_tot_onderhoud'], nieuwe_installatie['mail_verstuurd']))
                    return jsonify(c.lastrowid)
                else:
                    return jsonify({"error":"missing key"})

            elif request.method == 'PUT':
                nieuwe_installatie = valideer_installatie_request(request, "PUT")
                if nieuwe_installatie:
                    c.execute("UPDATE installaties set klant = ?,adres = ?,type = ?,datum = ?, laatste_onderhoud = ?,onderhoud_peko = ?,onderhoud_atag = ?,p_nummer = ?,dagen_tot_onderhoud = ?,mail_verstuurd = ? where id = ?", [nieuwe_installatie['klant'], nieuwe_installatie['adres'], nieuwe_installatie['type'] ,nieuwe_installatie['datum_installatie'],nieuwe_installatie['laatste_onderhoud'], nieuwe_installatie['onderhoud_peko'], nieuwe_installatie['onderhoud_atag'], nieuwe_installatie['p_nummer'], nieuwe_installatie['dagen_tot_onderhoud'], nieuwe_installatie['mail_verstuurd'], nieuwe_installatie['id']])
                    return jsonify({"message":"succes"})
                else:
                    return jsonify({"error":"missing key"})
                    
    except Exception as e:
        print(e)

@app.route("/upcoming", methods=['GET'])
def upcoming():
    try:
        if request.method == 'GET':
            with sqlite3.connect(db) as con:
                c = con.cursor()
                c.execute('select *, (laatste_onderhoud + (dagen_tot_onderhoud * 86400)) - cast(strftime("%s", "now") as decimal) as T from installaties order by T ASC')
                upcoming_dict = [{"id":k[0],"klant":k[1],"adres":k[2],"type":k[3],"datum_intallatie":k[4],"laatste_onderhoud":k[5],"onderhoud_peko":k[6],"onderhoude_atag":k[7],"p_nummer":k[8],"dagen_tot_onderhoud":k[9],"mail_verstuurd":k[10],"T":k[11]} for k in c.fetchall()]
                return jsonify(upcoming_dict)
    except Exception as e:
        print(e)


# request validation
def valideer_installatie_request(r, t):
    if t == "POST":
        if all(key in r.json.keys() for key in ['klant','adres','type','datum_installatie','laatste_onderhoud','onderhoud_peko','onderhoud_atag','p_nummer','dagen_tot_onderhoud','mail_verstuurd']):
            gevalideerde_installatie = r.json
            gevalideerde_installatie['datum_installatie'] = r.json.get('datum_installatie') if r.json.get('datum_installatie') != '' else time.mktime(datetime.date.today().timetuple())
            gevalideerde_installatie['laatste_onderhoud'] = r.json.get('laatste_onderhoud') if r.json.get('laatste_onderhoud') != '' else time.mktime(datetime.date.today().timetuple())
            gevalideerde_installatie['mail_verstuurd'] = 0
            return gevalideerde_installatie
        else: 
            return False
    elif t == "PUT":
        if all(key in r.json.keys() for key in ['id','klant','adres','type','datum_installatie','laatste_onderhoud','onderhoud_peko','onderhoud_atag','p_nummer','dagen_tot_onderhoud','mail_verstuurd']):
            gevalideerde_installatie = r.json
            with sqlite3.connect(db) as con:
                c = con.cursor()
                c.execute("select laatste_onderhoud from installaties where id = ?;", [gevalideerde_installatie['id']])
                if c.fetchone()[0] != gevalideerde_installatie['laatste_onderhoud']:
                    gevalideerde_installatie['mail_verstuurd'] = 0
            return gevalideerde_installatie
        else: 
            return False


# reminder
def get_te_onderhouden_installaties():
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute('select * from installaties where (laatste_onderhoud + (dagen_tot_onderhoud * 86400)) <= cast(strftime("%s", "now") as decimal) and mail_verstuurd = 0')
        installaties_dict = [{"id":k[0],"klant":k[1],"adres":k[2],"type":k[3],"datum_intallatie":k[4],"laatste_onderhoud":k[5],"onderhoud_peko":k[6],"onderhoude_atag":k[7],"p_nummer":k[8],"dagen_tot_onderhoud":k[9],"mail_verstuurd":k[10]} for k in c.fetchall()]
        if len(installaties_dict) != 0:
            send_mail(installaties_dict)

# mails
def send_mail(installaties):
    #mails...

    # update db for send mails
    with sqlite3.connect(db) as con:
        c = con.cursor()
        ids = [i['id'] for i in installaties]
        c.execute(f'update installaties set mail_verstuurd = 1 where id in (?{",?"*(len(ids)-1)})',[i['id'] for i in installaties])


get_te_onderhouden_installaties()

# Setup

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
