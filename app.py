from flask import Flask, render_template, request, redirect, session, flash
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "backup_nøkkel")

@app.route('/')
def forside():
     return render_template('index.html')



if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)