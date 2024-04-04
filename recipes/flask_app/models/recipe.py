from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import accounts
from flask import flash, session, redirect, render_template
from flask_app import app


db='recipes'
class recipe_class:
    def __init__( self , db_data ):
        self.id = db_data['id']
        self.name=db_data['name']
        self.description=db_data['description']
        self.instructions=db_data['instructions']
        self.date_made=db_data['date_made']
        self.under30=db_data['under30']
        self.accounts_id=db_data['accounts_id']
        self.creator = None

        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN accounts ON recipes.accounts_id = accounts.id;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for row in results:
            this_recipe = cls(row)
            accounts_data = {
                "id": row['id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            this_recipe.creator = accounts.accounts_class(accounts_data)
            recipes.append(this_recipe)
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM recipes JOIN accounts on recipes.accounts_id = accounts.id WHERE recipes.id = %(id)s;"""
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        result = result[0]
        this_recipe = cls(result)
        accounts_data = {
            "id": result['id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "password": "",
            "created_at": result['created_at'],
            "updated_at": result['updated_at']
        }
        this_recipe.creator = accounts.accounts_class(accounts_data)
        return this_recipe
    
    
    @classmethod
    def save(cls, form_data):
        query = """INSERT INTO recipes (name,description,instructions,date_made,under30,accounts_id)
                VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under30)s,%(accounts_id)s);"""
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def delete(cls,data):
        query = """DELETE FROM recipes WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query,data)
    
    
    @staticmethod
    def validate_recipe(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False
        if form_data['date_made'] == '':
            flash("when was this recipe made?")
            is_valid = False
        if 'under30' not in form_data:
            flash("Is it over or under?")
            is_valid = False

        return is_valid
    
    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE recipes
                SET name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s ,
                date_made = %(date_made)s,
                under_30 = %(under30)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
