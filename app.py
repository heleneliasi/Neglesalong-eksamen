from flask import Flask, render_template, request, redirect, session, flash
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)  #last .env fila

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "backup_nøkkel")

@app.route('/')
def index():
     return render_template('index.html')

@app.route("/services", methods=["GET", "POST"])
def services_side():
     mydb = get_connection()
     cursor = mydb.cursor()
     cursor.execute("SELECT * FROM service")
     services = cursor.fetchall()
     mydb.close()
     return render_template("service.html", services=services)

@app.route("/book", methods=["GET", "POST"])
def login_registrer():
     if "user_id" not in session:
          flash("Du må logge inn for å bestille time")
          return redirect("/login")
     
     mydb = get_connection()
     cursor = mydb.cursor()

     if request.method == "POST":
          service_id = request.form["service"]
          date = request.form["dato"]
          time = request.form["tid"]

          cursor.execute(
               "INSERT INTO appointment (user_id, service_id, date, time) VALUES (%s,%s,%s,%s)",
               (session["user_id"], service_id, date, time)
          )
          mydb.commit()

          cursor.execute("SELECT name FROM service WHERE id=%s", (service_id,))
          service = cursor.fetchone()
          mydb.close()

          return render_template("confirmation.html",
                navn=session["username"],
                tjeneste=service[0],
                dato=date,
                tid=time
            )
     
     cursor.execute("SELECT * FROM service")
     services = cursor.fetchall()
     mydb.close()

     return render_template("book.html", services=services)










if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)