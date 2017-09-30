import secrets
from flask import request, render_template, redirect, url_for, flash, session
from shoppinglist import app
from shoppinglist.models.dashboard import Dashboard
from shoppinglist.models.item import Item
from shoppinglist.models.shoppinglist import ShoppingList

dashboard = Dashboard()
app.secret_key = secrets.token_hex(32)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if name and email and password and confirm_password:
            if password != confirm_password:
                return render_template("signup.html", error="password mismatch: try again")

            if dashboard.signup(name, email, password):
                # if we have registered the user, let's try logging them in
                flash("You have been registered!")
                return redirect(url_for('login'))
            return render_template("signup.html", error=f"user with {email} already exists, log in please")
        return render_template("signup.html", error="all fields required! check to see if all boxes have been filled")
    return render_template("signup.html", error=None)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get("logged in"):
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            if dashboard.login(email, password):
                flash("Login successful")
                session["email"] = email
                return redirect(url_for("home"))
            return render_template("login.html", error="password incorrect! please try again")
        return render_template("login.html", error="missing fields: email and password")
    return render_template("login.html", error=None)


@app.route("/home", methods=['GET', 'POST'])
def home():
    """display shopping lists that the user has...
    Displays them in a table with links to edit and delete the links"""
    if not session.get("logged in"):
        return redirect(url_for("login"))
    user = dashboard.registry[session["email"]]
    return render_template("home.html", user=user, shoppinglists=user.shoppinglists)


@app.route("/shoppinglist/items/<list_id>", methods=["GET", "POST"])
def items(list_id):
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    shoppinglist = user.get_shoppinglist(list_id)
    if shoppinglist:
        return render_template("items.html", user=user, shoppinglist=shoppinglist)
    return redirect(url_for("home"))  # don't leave room for an error
