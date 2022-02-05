from app import app
from flask import render_template, request, redirect
import users
import sections


@app.route("/")
def index():
    return render_template("index.html", sections=sections.get_sections())


# SECTION ROUTES START

@app.route("/new_section", methods=["post"])
def new_section():
    users.require_role(1)

    section_name = request.form["section_name"]

    if len(section_name) < 4 or len(section_name) > 100:
        return render_template("error.html", message="Alueen nimen tulee olla 4-100 merkkiä")

    hidden_section = request.form.get("hidden_section")
    if hidden_section:
        # 1 = hidden
        hidden_section = 1
    else:
        hidden_section = 0

    sections.new_section(section_name, hidden_section)

    return redirect("/")


@app.route("/add_user_to_section", methods=["post"])
def add_user_to_section():
    users.require_role(1)

    section_id = request.form["section_id"]
    username = request.form["username"]

    if len(username) < 4 or len(username) > 20:
        return render_template("error.html", message="Tunnuksessa tulee olla 4-20 merkkiä")

    user_id = users.get_id_by_name(username)
    if user_id == -1:
        return render_template("error.html", message="Käyttäjää " + str(username) + " ei löytynyt")

    sections.add_user_to_section(section_id, user_id)

    return redirect("/")


# USER ROUTES START


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/login", methods=["post"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if len(username) < 4 or len(username) > 20:
        return render_template("error.html", message="Tunnuksessa tulee olla 4-20 merkkiä")

    if len(password) > 40 or len(password) < 8:
        return render_template("error.html", message="Salasanan tulee olla 8-40 merkkiä")

    if not users.login(username, password):
        return render_template("error.html", message="Väärä tunnus tai salasana")
    return redirect("/")


@app.route("/register", methods=["post"])
def register():
    username = request.form["username"]
    if len(username) < 4 or len(username) > 20:
        return render_template("error.html", message="Tunnuksessa tulee olla 4-20 merkkiä")

    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", message="Salasanat eroavat")
    if password1 == "":
        return render_template("error.html", message="Salasana on tyhjä")
    if len(password1) > 40 or len(password1) < 8:
        return render_template("error.html", message="Salasanan tulee olla 8-40 merkkiä")

    role = request.form.get("role")
    if role:
        # Admin
        role = 1
    else:
        # User
        role = 0

    if not users.register(username, password1, role):
        return render_template("error.html", message="Rekisteröinti ei onnistunut")
    return redirect("/")
