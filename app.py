from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_weight", methods=["POST"])
def add_weight():
    weight = request.form["weight"]
    db = get_db()
    db.execute("INSERT INTO progress (weight) VALUES (?)", (weight,))
    db.commit()
    return redirect("/progress")

@app.route("/progress")
def progress():
    db = get_db()
    data = db.execute("SELECT * FROM progress").fetchall()
    return render_template("progress.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)