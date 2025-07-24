from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    id_proof TEXT NOT NULL,
                    darshan_type TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time_slot TEXT NOT NULL,
                    tickets INTEGER NOT NULL
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        session['darshan_type'] = request.form['darshan_type']
        session['date'] = request.form['date']
        session['time_slot'] = request.form['time_slot']
        session['tickets'] = request.form['tickets']
        return redirect(url_for('details'))
    return render_template("book.html")

@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        id_proof = request.form['id_proof']
        darshan_type = session['darshan_type']
        date = session['date']
        time_slot = session['time_slot']
        tickets = session['tickets']

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, age, gender, id_proof, darshan_type, date, time_slot, tickets) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, age, gender, id_proof, darshan_type, date, time_slot, tickets))
        conn.commit()
        conn.close()
        return redirect(url_for('summary'))
    return render_template("details.html")

@app.route('/summary')
def summary():
    return render_template("summary.html")

@app.route('/bookings')
def bookings():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    data = c.fetchall()
    conn.close()
    return render_template("bookings.html", bookings=data)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
