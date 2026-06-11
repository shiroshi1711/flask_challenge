from flask import Flask, render_template, redirect, request
import sqlite3

conn = sqlite3.connect("pets.db",check_same_thread=False)

cursor = conn.cursor()

app = Flask(__name__)

cursor.execute("""
                CREATE TABLE IF NOT EXISTS pets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                species TEXT)""")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods =["POST"])
def add():
    name = request.form["pet_name"]
    species = request.form["species"]
    cursor.execute("""
                   INSERT INTO pets (name, species)
                   VALUES (?,?)""", (name, species))
    conn.commit()
    return redirect("/pets")

@app.route("/delete/<name>")
def delete(name):
    cursor.execute("""DELETE FROM pets
                   WHERE name = ?""",
                   (name,))
    conn.commit()
    return redirect("/pets")
    

@app.route("/pets")
def pets():
    cursor.execute("SELECT * FROM pets")
    all_pets = cursor.fetchall()
    return render_template("pets.html",pets=all_pets)

app.run(debug=True)