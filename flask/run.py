# Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import uuid, time, datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# App

app = Flask(__name__)
CORS(app)

# SQLite setup

db = "/database/PekoInstallations.db"

try:
    f = open(db)
except FileNotFoundError:
    print("No database found")
else:
    print("Database found")
    f.close()

# smtp setup

port = 465  # For SSL
try:
    with open('/run/secrets/db_pass') as secret:
        password = secret.readline()
except Exception as e:
    print(e)
context = ssl.create_default_context()
smtp_server = "smtp.gmail.com"
login = "gamesdezotn@gmail.com"
sender_email = "herinnering@peko.be"  # Enter your address
receiver_email = "k.tolpe@hotmail.com"  # Enter receiver address

# Routes

@app.route("/")
def init():
    return jsonify('Initializing')

# ---------------
# New Code
# ---------------

@app.route("/customers", methods=['GET', 'POST'])
def customers():
    try:
        with sqlite3.connect(db) as conn:

            c = conn.cursor()

            if request.method == 'GET':

                customer_cursor = c.execute("select * FROM klanten as k order by k.naam desc")
                all_customers = [{"id": customer[0], "name": customer[1], "phone": customer[2], "mail": customer[3]} for customer in customer_cursor]

                print(all_customers)

                return jsonify(all_customers)

            elif request.method == 'POST':

                json = request.get_json()
                customer_cursor = c.execute("INSERT INTO klanten VALUES (?, ?, ?, ?)", [str(uuid.uuid4()), json['name'], json['phone'], json['mail'], ])
                conn.commit()

                return jsonify(json)

            c.close()
            conn.close()

            return jsonify("Error")

    except Exception as e:
        print(e)
        return None


@app.route("/customers/<customer_id>", methods=['GET', 'PUT'])
def customer(customer_id):
    try:
        with sqlite3.connect(db) as conn:

            c = conn.cursor()

            if request.method == 'GET':

                customer_cursor = c.execute("select * FROM klanten where id = ?", [customer_id])
                customer = [{"id": c[0], "name": c[1], "phone": c[2], "mail": c[3]} for c in customer_cursor]

                return jsonify(customer)

            elif request.method == 'PUT':

                json = request.get_json()
                customer_cursor = c.execute("update klanten set naam = ?, telefoon = ?, mail = ? where id = ?", [json["name"], json["phone"], json["mail"], customer_id])
                customer = [{"id": c[0], "name": c[1], "phone": c[2], "mail": c[3]} for c in customer_cursor]

                return jsonify(customer)

            c.close()
            conn.close()

    except Exception as e:
        print(e)
        return None


@app.route("/installations", methods=['GET'])
def installations():
    try:
        with sqlite3.connect(db) as conn:

            c = conn.cursor()

            if request.method == 'GET':

                installation_cursor = c.execute("select * FROM installaties as i order by i.datum desc ")
                all_installations = []
                unique_customers = set()
                for inst in installation_cursor:
                    if inst[1] in unique_customers:
                        for customer in all_installations:
                            if customer['id'] == inst[1]:
                                customer['installations'].append({"id": inst[0], "adres": inst[2], "type": inst[3], "datum_installatie": inst[4], "laatste_onderhoud": inst[5], "p_nummer": inst[8], "reminder": inst[9]})
                    else:
                        unique_customers.add(inst[1])
                        all_installations.append({"id": inst[1], "installations": [{"id": inst[0], "adres": inst[2], "type": inst[3], "datum_installatie": inst[4], "laatste_onderhoud": inst[5], "p_nummer": inst[8], "reminder": inst[9]}]})
                print(all_installations)
                return jsonify(all_installations)

            c.close()
            conn.close()

            return jsonify("Error")

    except Exception as e:
        print("Error: " + str(e))
        return jsonify("Error, Something went wrong")


# ---------------
# Old Code
# ---------------

@app.route("/klanten", methods=['GET','POST', 'PUT'])
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


@app.route("/installaties", methods=['POST','PUT'])
def installaties():
    try:
        with sqlite3.connect(db) as con:
            c = con.cursor()
            if request.method == 'POST':
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

@app.route("/installaties/<klant_id>", methods=['GET'])
def installaties_klant(klant_id):
    try:
        with sqlite3.connect(db) as con:
            c = con.cursor()
            if request.method == 'GET':
                c.execute("select * FROM installaties where klant = ?",[klant_id])
                installaties_dict = [{"id":k[0],"klant":k[1],"adres":k[2],"type":k[3],"datum_intallatie":k[4],"laatste_onderhoud":k[5],"onderhoud_peko":k[6],"onderhoude_atag":k[7],"p_nummer":k[8],"dagen_tot_onderhoud":k[9],"mail_verstuurd":k[10]} for k in c.fetchall()]
                return jsonify(installaties_dict)

                    
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
        c.execute('select k.*, i.* from installaties as i inner JOIN klanten as k on i.klant = k.id where (laatste_onderhoud + (dagen_tot_onderhoud * 86400)) <= cast(strftime("%s", "now") as decimal) and mail_verstuurd = 0')
        send_mail(c.fetchall())

# mails
def send_mail(installaties):
    #mails...
    if len(installaties) > 0:
        all_installations = []
        unique_customers = set()
        for inst in installaties:
            if inst[0] in unique_customers:
                for customer in all_installations:
                    if customer['id'] == inst[0]:
                        customer['installations'].append({"adres": inst[6], "type": inst[7], "datum_installatie": inst[8], "laatste_onderhoud": inst[9], "p_nummer": inst[12], "reminder": inst[13]})
            else:
                unique_customers.add(inst[0])
                all_installations.append({"id": inst[0], "naam": inst[1], "telefoon": inst[2], "mail": inst[3], "installations": [{"adres": inst[6], "type": inst[7], "datum_installatie": inst[8], "laatste_onderhoud": inst[9], "p_nummer": inst[12], "reminder": inst[13]}]})
        html = ""
        for k in all_installations:
            html += "Klant: {}\nInstallatie(s):\n\n".format(k['naam'])
            for i in k['installations']:
                datum_i = datetime.datetime.fromtimestamp(i['datum_installatie'])
                datum_lo = datetime.datetime.fromtimestamp(i['laatste_onderhoud'])
                td = (datetime.datetime.today() -datum_lo).days
                html += "\tAdres: {}      Type: {}\t P nummer: {}\n\tDatum installatie: {}        Laatste onderhoud: {}       Dagen sinds onderhoud: {}\n\n".format(i['adres'], i['type'], i['p_nummer'], datum_i.date(),datum_lo.date(), td)

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(login, password)
            message = MIMEMultipart("alternative")
            message["Subject"] = "Herinnering ketel installatie"
            message["From"] = sender_email
            message["To"] = receiver_email
            message.attach(MIMEText(html, "plain"))
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
        # update db for send mails
        with sqlite3.connect(db) as con:
            c = con.cursor()
            ids = [i['id'] for i in installaties]
            c.execute(f'update installaties set mail_verstuurd = 1 where id in (?{",?"*(len(ids)-1)})',[i['id'] for i in installaties])


get_te_onderhouden_installaties()

# Setup

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
