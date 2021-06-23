from flask_app import app
from flask import render_template, request, redirect, session

from flask_app.models.trainer import Trainer
from flask_app.models.pokemon import Pokemon

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash


# ================================================


@app.route("/")
def index():
    return render_template("index.html")



# ================================================
# Register Route
# ================================================
@app.route("/register", methods=["POST"])
def register():
    # checking the validation parameters
    if not Trainer.validate_trainer(request.form):
        return redirect("/")
    # checking to see if the email exists
    data1 = {
        "email" : request.form["email"]
    }
    if Trainer.get_trainer_by_email(data1):
        flash("Email already exists, need to register a differnt email")
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }

    trainer_id = Trainer.save(data)

    session["trainer_id"] = trainer_id
    return redirect("/dashboard")
    # ================================================

# ================================================
# Login Route
# ================================================

@app.route("/login", methods=["POST"])
def login():
    data = {
        "email" : request.form["email"]
    }
    user_in_db = Trainer.get_trainer_by_email(data)
    if not user_in_db:
        flash("Invalid Credentials")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Credentials")
        return redirect("/")

    session['trainer_id'] = user_in_db.id
    return redirect("/dashboard")
    # ================================================

@app.route("/dashboard")
def dashboard():
    if "trainer_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")
    
    data = {
        "id" : session["trainer_id"]
    }
    logged_user = Trainer.get_one_trainer(data)

    pokemons = Pokemon.all_pokemons()
    return render_template("/dashboard.html", trainer = logged_user, pokemons = pokemons)
    # ================================================



# ================================================
# Logout Route
# ================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
    # ================================================