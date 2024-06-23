import os

from cs50 import SQL
from flask import Flask, render_template, redirect, session, request
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, apology

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///auditions.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        db = SQL("sqlite:///finance.db")
        username = request.form.get("username")
        if not username:
            return apology("Username required")

        password = request.form.get("password")
        if not password:
            return apology("Password required.")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Must enter password second time")

        if password != confirmation:
            return apology("Passwords must match")

        else:
            hashPass = generate_password_hash(request.form.get("password"))
            try:
                db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hashPass)
            except ValueError:
                return apology("Username already exists")
            return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Username required")

        password = request.form.get("password")
        if not password:
            return apology("Password required")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")