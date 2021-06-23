from flask_app import app
from flask import render_template, request, redirect, session

from flask_app.models.trainer import Trainer
from flask_app.models.pokemon import Pokemon

from flask import flash

# ================================================
# Create Pokemon Routes
# ================================================
@app.route("/pokemon/new")
def create_pokemon():
    if "trainer_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")
    trainer_id = session["trainer_id"]
    return render_template("create_pokemon.html", trainer_id = trainer_id)
    # ================================================

@app.route("/add_pokemon", methods=["POST"])
def add_pokemon():
    if not Pokemon.validate_pokemon(request.form):
        return redirect("/pokemon/new")

    data = {
        "name" : request.form['name'],
        "number" : request.form['number'],
        "type" : request.form['type'],
        "description" : request.form['description'],
        "trainer_id" : request.form['trainer_id']
    }
    Pokemon.save(data)
    return redirect("/dashboard")
    # ================================================


# ================================================
# View Pokemon Routes
# ================================================
@app.route("/pokemon/<int:id>")
def view_one(id):
    if "trainer_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")

    data = {
        "id" : id
    }
    pokemon = Pokemon.one_pokemon(data)


    data = {
        "id" : session["trainer_id"]
    }
    logged_user = Trainer.get_one_trainer(data)
    return render_template("view_pokemon.html", trainer = logged_user, pokemon = pokemon)


# ================================================
# Edit Pokemon Routes
# ================================================

@app.route("/pokemon/edit/<int:id>")
def edit_one(id):
    if "trainer_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")

    data = {
        "id" : id
    }
    pokemon = Pokemon.one_pokemon(data)
    return render_template("edit_pokemon.html", pokemon = pokemon)

@app.route("/update_pokemon/<int:id>", methods=["POST"])
def update_pokemon(id):
    if not Pokemon.validate_pokemon(request.form):
        return redirect(f"/update_pokemon/{id}")
    
    data = {
        "name" : request.form['name'],
        "number" : request.form['number'],
        "type" : request.form['type'],
        "description" : request.form['description'],
        "trainer_id" : request.form['trainer_id'], 
        "id" : id
    }
    Pokemon.update_one_pokemon(data)

    return redirect("/dashboard")

# ================================================
# Delete Pokemon Routes
# ================================================

@app.route("/pokemon/delete/<int:id>")
def delete_pokemon(id):
    data = {
        "id" : id
    }
    Pokemon.delete(data)
    return redirect("/dashboard")