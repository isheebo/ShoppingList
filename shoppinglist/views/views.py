import secrets
from flask import request, render_template, redirect, url_for, flash, session
from shoppinglist import app
from shoppinglist.models.dashboard import Dashboard

dashboard = Dashboard()
app.secret_key = secrets.token_hex(32)


@app.route("/")
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
                flash(f"user with email {email} has been registered!")
                return redirect(url_for('login'))
            return render_template("signup.html", error=f"user with {email} already exists, log in please")
        return render_template("signup.html", error="all fields required! check to see if all boxes have been filled")
    return render_template("signup.html", error=None)  # when request.method == 'GET'


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get("logged in"):  # if a user is already logged in
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            if len(dashboard.registry) == 0:
                return render_template('login.html',
                                       error='unknown email: you need to first signup before you can log in')

            if dashboard.login(email, password):
                flash(f"Login successful for {email}")
                session["logged in"] = True
                session["email"] = email
                return redirect(url_for("home"))
            return render_template("login.html", error="password incorrect! please try again")
        return render_template("login.html", error="missing fields: both email and password are required")
    return render_template("login.html", error=None)  # when request.method == 'GET'


@app.route("/view/lists", methods=['GET', 'POST'])
def home():
    """ displays the shopping lists that the user has...
    Displays them in a table with links to edit and delete the lists. """

    if not session.get("logged in"):
        return redirect(url_for("login"))
    user = dashboard.registry[session["email"]]
    return render_template("home.html", user=user, shoppinglists=user.shoppinglists)


@app.route("/add/list/", methods=['POST'])
def add_list():
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    list_name = request.form.get("name")
    notify_date = request.form.get("notify_date")
    list_id = secrets.token_urlsafe(10)

    if list_name and notify_date:
        if user.create_shoppinglist(list_id, list_name, notify_date):
            flash(f"List with name '{list_name.title()}' has been created")
        else:
            flash(f"A shopping list with its name as '{list_name}' already exists")
    else:
        flash("unable to create list: please enter a valid list name")
    return redirect(url_for('home'))


@app.route("/edit/list/<list_id>", methods=['GET', 'POST'])
def edit_list(list_id):
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    shoppinglist = user.get_shoppinglist(list_id)

    if not shoppinglist:
        flash("shoppinglist not found!")
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get("name")
        notify_date = request.form.get("notify_date")
        if shoppinglist.name != name.title() or shoppinglist.notify_date != notify_date:
            if user.edit_shoppinglist(shoppinglist.id, name, notify_date):
                flash("List edited successfully")
            else:
                flash(f"a shopping list with that name ('{name.title()}') already exists")
            return redirect(url_for('home'))
        flash('no changes have been made to the list!')
        return redirect(url_for('home'))
    return render_template('edit_list.html', user=user, shoppinglist=shoppinglist)


@app.route("/delete/list/<list_id>", methods=['GET', 'POST'])
def delete_list(list_id):
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    shoppinglist = user.get_shoppinglist(list_id)

    if not shoppinglist:
        flash("shoppinglist not found!")
        return redirect(url_for('home'))

    if request.method == 'POST':
        if user.delete_shoppinglist(shoppinglist.id):
            flash("List has been successfully deleted")
            return redirect(url_for("home"))
    return render_template('delete_list.html', user=user, shoppinglist=shoppinglist)


@app.route("/list/items/<list_id>", methods=["GET", "POST"])
def items(list_id):
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    shoppinglist = user.get_shoppinglist(list_id)

    # regardless of the request method
    if not shoppinglist:
        return redirect(url_for("home"))  # don't leave room for an error: redirect to the shoppinglists view
    return render_template("items.html", user=user, shoppinglist=shoppinglist)


@app.route("/add/list/items/<list_id>", methods=['POST'])
def add_item(list_id):
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    shoppinglist = user.get_shoppinglist(list_id)

    if shoppinglist:
        name = request.form.get("name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        if name and price and quantity:
            item_id = secrets.token_urlsafe(10)
            if shoppinglist.add_item(item_id, name, price, quantity):
                return redirect(url_for("items", list_id=shoppinglist.id))
            flash(f"item with name '{name}' already exists!")
        return redirect(url_for("items", list_id=shoppinglist.id))
    return redirect(url_for("home", user=user, shoppinglists=user.shoppinglists))


@app.route("/edit/list/items/<list_id>/<item_id>", methods=['GET', 'POST'])
def edit_item(list_id, item_id):
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    shoppinglist = user.get_shoppinglist(list_id)

    if not shoppinglist:
        flash("shopping list not found!")
        return redirect(url_for("home", user=user, shoppinglists=user.shoppinglists))

    item = shoppinglist.get_item(item_id)

    if shoppinglist and not item:
        # flash("item does not exist on this shopping list")
        return redirect(url_for('items', list_id=shoppinglist.id))

    if request.method == 'POST':
        name = request.form.get("name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        if item.name != name.title() or item.quantity != quantity or item.price != price:
            if shoppinglist.edit_item(item_id, name, price, quantity):
                flash("Item edit successful")
            else:
                flash(f"failed to edit Item: an item with name '{name}' already exists")
            return redirect(url_for('items', list_id=shoppinglist.id))
        flash("no changes were made to the item")
        return redirect(url_for('items', list_id=shoppinglist.id))
    return render_template('edit_item.html', user=user, shoppinglist=shoppinglist, item=item)


@app.route("/delete/list/items/<list_id>/<item_id>", methods=['GET', 'POST'])
def delete_item(list_id, item_id):
    if not session.get("logged in"):
        return redirect(url_for("login"))

    user = dashboard.registry[session["email"]]
    shoppinglist = user.get_shoppinglist(list_id)

    if not shoppinglist:
        flash("shopping list not found!")
        return redirect(url_for("home", user=user, shoppinglists=user.shoppinglists))

    item = shoppinglist.get_item(item_id)

    if shoppinglist and not item:
        # flash("item does not exist on this shopping list")
        return redirect(url_for('items', list_id=shoppinglist.id))

    if request.method == 'POST':
        if shoppinglist.remove_item(item.id):
            flash("Item deleted successfully")
            return redirect(url_for('items', list_id=shoppinglist.id))
    return render_template("delete_item.html", user=user, shoppinglist=shoppinglist, item=item)


@app.route("/logout")
def logout():
    if session.get("logged in"):
        del session["email"]
        session["logged in"] = False
        dashboard.logout()
    return redirect(url_for('login'))
