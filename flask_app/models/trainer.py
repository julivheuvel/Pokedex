from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# =====================================================


class Trainer: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # ================================================

    @staticmethod
    def validate_trainer(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long!")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters long!")
            is_valid = False
        if len(data['email']) < 7:
            flash("Email must be at least 7 characters long!")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email is not valid!")
            is_valid = False
        if len(data['password']) < 3:
            flash("Password must be at least 3 characters long!")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid
        # ================================================

    @classmethod
    def get_one_trainer(cls, data):
        query = "SELECT * FROM trainers WHERE id = %(id)s;"
        results = connectToMySQL('trainers_pokemons_schema').query_db(query, data)
        return cls(results[0])
        # ================================================

    @classmethod
    def get_trainer_by_email(cls, data):
        query = "SELECT * FROM trainers WHERE email = %(email)s;"
        results = connectToMySQL('trainers_pokemons_schema').query_db( query, data )
        if len(results) < 1:
            return False
        return cls(results[0])
        # ================================================

    @classmethod
    def save(cls, data):
        query = "INSERT INTO trainers ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"
        return connectToMySQL('trainers_pokemons_schema').query_db( query, data )
        # ================================================

