from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import trainer

# =======================================================

class Pokemon:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.number = data['number']
        self.type = data['type']
        self.description = data['description']
        self.trainer_id = data['trainer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # ================================================
        self.posted_by = {}
        # ================================================

    @staticmethod
    def validate_pokemon(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Name must be at least 2 characters long!")
            is_valid = False
        if len(data['type']) < 3:
            flash("Type must be at least 3 characters long!")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters long!")
            is_valid = False
        return is_valid
        # ================================================

    @classmethod
    def save(cls, data):
        query = "INSERT INTO pokemons ( name , number , type , description, trainer_id, created_at, updated_at ) VALUES ( %(name)s , %(number)s , %(type)s , %(description)s , %(trainer_id)s, NOW() , NOW() );"
        return connectToMySQL('trainers_pokemons_schema').query_db( query, data )
        # ================================================
    
    @classmethod
    def all_pokemons(cls):
        query = "SELECT * FROM pokemons;"
        results = connectToMySQL('trainers_pokemons_schema').query_db( query )

        recipes = []
        for one_recipe in results:
            recipes.append( cls(one_recipe))
        return recipes
        # ================================================
    
    @classmethod
    def one_pokemon(cls, data):
        query = "SELECT * FROM pokemons JOIN trainers ON trainers.id = trainer_id WHERE pokemons.id = %(id)s;"
        results = connectToMySQL('trainers_pokemons_schema').query_db( query, data )
        pokemon = cls(results[0])
        trainer_data = {
            "id" : results[0]['trainers.id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['trainers.created_at'],
            "updated_at" : results[0]['trainers.updated_at']
        }
        pokemon.posted_by = trainer.Trainer(trainer_data)
        return pokemon
        # ================================================

    @classmethod
    def update_one_pokemon(cls, data):
        query = "UPDATE pokemons SET name = %(name)s, number = %(number)s, type = %(type)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL('trainers_pokemons_schema').query_db( query, data )
        return results
        # ================================================
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pokemons WHERE id = %(id)s;"
        results = connectToMySQL('trainers_pokemons_schema').query_db( query, data )
        return results