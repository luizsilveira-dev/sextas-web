from flask import Flask, flash, render_template, request, jsonify, redirect, url_for
import sqlite3, datetime
from routes.query_routes import query_bp
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)
# app.register_blueprint(query_bp)

app.secret_key = os.getenv("FLASK_SECRET")

def init_db():
    conn = sqlite3.connect("dados.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sextas (
            data TEXT PRIMARY KEY,
            status TEXT
        )
    """)
    conn.close()

def get_fridays_status():
    conn = sqlite3.connect("dados.db")
    cur = conn.cursor()
    cur.execute("SELECT data, status FROM sextas")
    data = {row[0]: row[1] for row in cur.fetchall()}
    conn.close()
    return data

@app.route("/")
def index():
    hoje = datetime.date.today()
    ano = hoje.year
    dados = get_fridays_status()
    dias = []

    for mes in range(1, 13):
        for dia in range(1, 32):
            try:
                d = datetime.date(ano, mes, dia)
            except ValueError:
                continue
            if d.weekday() == 4:  # sexta-feira
                status = "futuro"
                if d < hoje:
                    status = "verde"
                dias.append((d, status))
            else:
                continue

    total = len(dias)
    passadas = len([d for d, s in dias if d < hoje])

    # Due to the consistency of the poster, there is no need to check for 
    # posted days, as we can be 100% sure that they will be posted.
    return render_template("index.html", dias=dias, ano=ano, total=total,
                           passadas=passadas, presentes=passadas)

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        data = request.form["data"]
        data_full = datetime.datetime.strptime(data, '%Y-%m-%d')
        if data_full.weekday() != 4:  # segunda=0, sexta=4
            flash('A data precisa ser uma sexta-feira!', 'erro')
            return redirect(url_for('adicionar'))
        status = request.form["status"]
        conn = sqlite3.connect("dados.db")
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO sextas (data, status) VALUES (?, ?)", (data, status))
        conn.commit()
        conn.close()
        return redirect(url_for("adicionar"))
    return render_template("adicionar.html")

@app.route("/api/dados")
def api_dados():
    hoje = datetime.date.today()
    ano = hoje.year
    dados = get_fridays_status()
    dias = []

    for mes in range(1, 13):
        for dia in range(1, 32):
            try:
                d = datetime.date(ano, mes, dia)
            except ValueError:
                continue
            if d.weekday() == 4:  # sexta-feira
                status = "futuro"
                if d < hoje:
                    status = "verde"
                dias.append((d, status))
            else:
                continue

    passadas = len([d for d, s in dias if d < hoje])

    # Due to the consistency of the poster, there is no need to check for 
    # posted days, as we can be 100% sure that they will be posted.
    return jsonify({'presentes' : presentes, 'passadas' : presentes})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8080, debug=True)
