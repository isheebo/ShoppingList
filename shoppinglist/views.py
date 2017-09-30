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