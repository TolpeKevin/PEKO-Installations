# Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import uuid, time, datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
import base64
import os
import logging

log_path = os.getenv("APPDATA")+"\\PEKO\\Log\\peko.log"

logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename=log_path, level=logging.DEBUG)

# App

app = Flask(__name__)
CORS(app)

# ---------------
# SQLite setup
# ---------------

db = os.getenv("APPDATA")+"\\PEKO\\Data\\PekoInstallations.db"

try:
    f = open(db)
except FileNotFoundError:
    logging.critical('database not found')
    exit()
else:
    f.close()
    logging.info("database found")


# ---------------
# smtp setup
# ---------------

port = 465  # For SSL
try:
    password = base64.b64decode(os.getenv('PEKO')).decode()
    logging.info("succesful authentication step 1")
except Exception as e:
    logging.error("Failure on authentication step 1 :"+ str(e))

context = ssl.create_default_context()
smtp_server = "smtp.gmail.com"
#smtp_server = "send.one.com"
#smtp_server = "mailout.one.com"
login = "gamesdezotn@gmail.com"
#login = "koen@pekoinstallations.be"
sender_email = "herinnering@peko.be"  # Enter your address
receiver_email = "k.tolpe@hotmail.com"  # Enter receiver address
#receiver_email = "koen@pekoinstallations.be"  # Enter receiver address

# ---------------
# Routes
# ---------------

@app.route("/")
def init():
    return jsonify('Initializing')


@app.route("/customers", methods=['GET', 'POST'])
def customers():
    logging.debug("/cutomer " + str(request.method))
    try:
        with sqlite3.connect(db) as conn:

            c = conn.cursor()

            if request.method == 'GET':
                customer_cursor = c.execute("select * FROM klanten as k order by k.naam desc")
                all_customers = [{"id": customer[0], "name": customer[1], "phone": customer[2], "mail": customer[3]} for customer in customer_cursor]

                return jsonify(all_customers)

            elif request.method == 'POST':
                json = request.get_json()

                customer_id = str(uuid.uuid4())
                customer_cursor = c.execute("INSERT INTO klanten VALUES (?, ?, ?, ?)", [customer_id, json['name'], json['phone'], json['mail'], ])
                for installation in json['installations']:
                    customer_cursor = c.execute("INSERT INTO installaties VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [str(uuid.uuid4()), customer_id, installation['address'], installation['type'], str_to_utc(installation['installation_date']), str_to_utc(installation['installation_date']), 0, 0, installation['pnumber'], installation['reminder'], 0])
                conn.commit()


            c.close()
            conn.close()

            return jsonify("Error")

    except Exception as e:
        logging.error("/customer : " + str(e))
        return jsonify("Error")


@app.route("/customers/<customer_id>", methods=['GET', 'PUT', 'DELETE'])
def customer(customer_id):
    logging.debug("/cutomer/id " + request.method)
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

            elif request.method == 'DELETE':

                customer_cursor = c.execute("delete from installaties as i where i.klant = ?", [customer_id])
                customer_cursor = c.execute("delete from klanten as k where k.id = ?", [customer_id])

                return jsonify("Succesfull")

            c.close()
            conn.close()

    except Exception as e:
        logging.error("/customer/id : " + str(e))
        return None


@app.route("/installations", methods=['GET','POST','PUT'])
def installations():
    logging.debug("/installations " + request.method)
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
                                customer['installations'].append({"id": inst[0], "adres": inst[2], "type": inst[3], "datum_installatie": utc_to_str(inst[4]), "laatste_onderhoud": utc_to_str(inst[5]), "p_nummer": inst[8], "reminder": inst[9]})
                    else:
                        unique_customers.add(inst[1])
                        all_installations.append({"id": inst[1], "installations": [{"id": inst[0], "adres": inst[2], "type": inst[3], "datum_installatie": utc_to_str(inst[4]), "laatste_onderhoud": utc_to_str(inst[5]), "p_nummer": inst[8], "reminder": inst[9]}]})
                return jsonify(all_installations)
            
            elif request.method == 'POST':

                json = request.get_json()
                for installation in json['installations']:
                    c.execute("INSERT INTO installaties VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [str(uuid.uuid4()), json['customer_id'], installation['address'], installation['type'], str_to_utc(installation['installation_date']), str_to_utc(installation['installation_date']), 0, 0, installation['pnumber'], installation['reminder'], 0])

                conn.commit()
                return jsonify("Succes")

            
            elif request.method == 'PUT':

                json = request.get_json()
                for installation in json['installations']:
                    c.execute("UPDATE installaties set (adres = ?, type = ?, datum = ?, laatste_onderhoud = ?, onderhoud_peko = ?, onderhoud_atag = ?, p_nummer = ?, dagen_tot_onderhoud = ?, mail_verstuurd =  ?)", [installation['address'], installation['type'], str_to_utc(installation['installation_date']), str_to_utc(installation['installation_date']), 0, 0, installation['pnumber'], installation['reminder'], check_mail(installation['id'],str_to_utc(installation['maintenance_date']))])

                conn.commit()
                return jsonify("Succes")

            c.close()
            conn.close()

            return jsonify("Errors")

    except Exception as e:
        logging.error("/installations : " + str(e))
        return jsonify("Error, Something went wrong")

@app.route("/installations/<costumer_id>", methods=['GET', 'PUT', 'DELETE'])
def installation(costumer_id):
    logging.debug("/installations/id " + request.method)
    try:
        with sqlite3.connect(db) as con:
            c = con.cursor()
            if request.method == 'GET':
                c.execute("select * FROM installaties where klant = ?",[costumer_id])
                installaties_dict = [{"id":k[0],"customer_id":k[1],"address":k[2],"type":k[3],"installation_date":utc_to_str_update(k[4]),"laatste_onderhoud":utc_to_str_update(k[5]),"onderhoud_peko":k[6],"onderhoud_atag":k[7],"p_nummer":k[8],"dagen_tot_onderhoud":k[9],"mail_verstuurd":k[10]} for k in c.fetchall()]
                return jsonify(installaties_dict)
            
            if request.method == 'PUT':
                json = request.get_json()
                for installation in json['installations']:
                    c.execute("UPDATE installaties set adres = ?, type = ?, datum = ?, laatste_onderhoud = ?, p_nummer = ?, dagen_tot_onderhoud = ?, mail_verstuurd =  ? where id like ?", [installation['address'], installation['type'], str_to_utc(installation['installation_date']), str_to_utc(installation['maintenance_date']), installation['pnumber'], installation['reminder'], check_mail(installation['id'],str_to_utc(installation['maintenance_date'])), installation['id']])
                con.commit()
                return jsonify("Succes")

            if request.method == 'DELETE':
                c.execute("delete from installaties as i where i.id = ?", [costumer_id])

                con.commit()
                return jsonify("Succes")



                    
    except Exception as e:
        logging.error("/installations/id : " + str(e))

# ---------------
# Old Code
# ---------------
@app.route("/upcoming", methods=['GET'])
def upcoming():
    logging.debug("/upcoming " + request.method)
    try:
        if request.method == 'GET':
            with sqlite3.connect(db) as con:
                c = con.cursor()
                c.execute('select klanten.naam, adres, type, laatste_onderhoud, p_nummer, dagen_tot_onderhoud, (laatste_onderhoud + (dagen_tot_onderhoud * 86400)) - cast(strftime("%s", "now") as decimal) as T from installaties INNER join klanten on installaties.klant = klanten.id order by T ASC')
                upcoming_dict = [{"klant":k[0],"adres":k[1],"type":k[2],"laatste_onderhoud":utc_to_str(k[3]),"p_nummer":k[4],"deadline":k[5],"T": timediff_to_str(k[6])} for k in c.fetchall()]
                return jsonify(upcoming_dict)
    except Exception as e:
        print(e)
        logging.error("/upcoming : "  + str(e))

# ---------------
# date conversion
# ---------------

def str_to_utc(str_date):
    logging.debug("converting to utc: "+ str(str_date))
    return str(int(datetime.datetime.strptime(str_date, '%Y-%m-%d').timestamp()))

def utc_to_str(utc_date):
    logging.debug("converting to str: "+ str(utc_date))
    return datetime.datetime.fromtimestamp(float(utc_date)).strftime('%d/%m/%Y')

def utc_to_str_update(utc_date):
    logging.debug("converting to str: "+ str(utc_date))
    return datetime.datetime.fromtimestamp(float(utc_date)).strftime('%Y-%m-%d')


def timediff_to_str(time_diff):
    return round(time_diff * 0.00001157407)
# ---------------
# update 'mail send' on items who received maintenance on PUT
# ---------------
def check_mail(installation_id, installation_maintenance):
    logging.debug("checking to send mail")
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute("select laatste_onderhoud from installaties where id = ?;", [installation_id])
        if c.fetchone()[0] != installation_maintenance:
            return 0
        else: 
            return 1


# ---------------
# mails for installations that need maintenance
# ---------------


def get_te_onderhouden_installaties():
    logging.debug("getting installations that need maintenance")
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute('select k.*, i.* from installaties as i inner JOIN klanten as k on i.klant = k.id where (laatste_onderhoud + (dagen_tot_onderhoud * 86400)) <= cast(strftime("%s", "now") as decimal) and mail_verstuurd = 0')
        send_mail(c.fetchall())

def send_mail(installaties):
    #mails...
    logging.debug("sending mails")
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
                datum_i = datetime.datetime.fromtimestamp(int(i['datum_installatie']))
                datum_lo = datetime.datetime.fromtimestamp(int(i['laatste_onderhoud']))
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
            logging.info("send mail")

        # update db for send mails
        with sqlite3.connect(db) as con:
            c = con.cursor()
            ids = [i[4] for i in installaties]
            c.execute(f'update installaties set mail_verstuurd = 1 where id in (?{",?"*(len(ids)-1)})',ids)


get_te_onderhouden_installaties()

scheduler = BackgroundScheduler()
scheduler.add_job(get_te_onderhouden_installaties, 'interval', hours=12)
scheduler.start()
# ---------------
# Setup
# ---------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

