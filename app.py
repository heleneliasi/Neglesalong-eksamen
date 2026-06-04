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
     return render_template("services.html", services=services)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        passord = request.form["password"]

        mydb = get_connection()
        cursor = mydb.cursor()

        cursor.execute(
            "SELECT id, username, password, role FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()
        mydb.close()

        if user and check_password_hash(user[2], passord):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            flash("Velkommen tilbake!")
            if session["role"] == "admin":
                return redirect("/admin")
            return redirect("/minside")
        
        flash("Feil email eller passord")

    return render_template("login.html")

@app.route("/admin")
def admin():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")
    
    mydb = get_connection()
    cursor = mydb.cursor()

    cursor.execute(
        "SELECT appointment.id, users.username, service.name, appointment.date, appointment.time "
        "FROM appointment "
        "JOIN users ON appointment.user_id = users.id "
        "JOIN service ON appointment.service_id = service.id"
    )
    


@app.route("/minside")
def minside():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") == "admin":
        return redirect("/admin")
    
    mydb = get_connection()
    cursor = mydb.cursor()

    cursor.execute(
        "SELECT service.name, appointment.date, appointment.time "
        "FROM appointment "
        "JOIN service ON appointment.service_id = service.id "
        "WHERE appointment.user_id = %s",
        (session["user_id"],)
    )
    timer = cursor.fetchall()
    mydb.close()

    return render_template("minside.html", timer=timer, navn=session["username"])


@app.route("/registrer", methods=["GET", "POST"])
def registrer():
    if request.method == "POST":
        navn = request.form["navn"]
        email = request.form["email"]
        passord = generate_password_hash(request.form["password"])

        mydb = get_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing = cursor.fetchone()

        if existing:
            flash("Email finnes allerede. Logg inn i stedet.")
            return redirect("/login")
        
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
            (navn, email, passord)
        )
        mydb.commit()

        session["user_id"] = cursor.lastrowid
        session["username"] = navn

        flash("Bruker opprettet! Du er nå innlogget.")
        return redirect("/book")

    return render_template("registrer.html")


@app.route("/book", methods=["GET", "POST"])
def book_side():
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


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/sendinn", methods=["GET", "POST"])
def sendinn():
    if request.method == "POST":
        navn = request.form.get("navn", "").strip()
        email = request.form.get("email", "").strip()
        sporsmal = request.form.get("sporsmal", "").strip()

        if not sporsmal:
            flash("Du må skrive inn et spørsmål.")
            return redirect("/sendinn")
        
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO questions (name, email, question) VALUES (%s, %s, %s)",
            (navn, email, sporsmal)
        )
        mydb.commit()
        mydb.close()

        flash("Takk! Spørsmålet ditt er sendt")
        return redirect("/faq")
    
    return render_template("sendinn.html")

@app.route("/slettbruker", methods=["GET", "POST"])
def slettbruker():
    if request.method == "POST":
        email = request.form["email"]
        passord = request.form["password"]

        mydb = get_connection()
        cursor = mydb.cursor()

        cursor.execute(
            "SELECT id, password FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user[1], passord):
            cursor.execute("DELETE FROM appointment WHERE user_id=%s", (user[0],))
            cursor.execute("DELETE FROM users WHERE id=%s", (user[0],))
            mydb.commit()
            mydb.close()
            session.clear()
            return redirect("/slettet")
        
        mydb.close()
        flash("Feil email eller passord")

    return render_template("slettbruker.html")


@app.route("/slettet")
def slettet():
    return render_template("slettet.html")


@app.route("/logout")
def loggut():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
