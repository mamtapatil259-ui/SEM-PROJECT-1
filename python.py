
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret"

# Demo user credentials
USERNAME = "admin"
PASSWORD = "admin123"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            session["username"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return f"""
    <h1>Welcome, {session['username']}!</h1>
    <p>You have successfully logged in.</p>
    <a href="/logout">Logout</a>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)