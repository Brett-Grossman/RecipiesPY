from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class accounts_class:
    db="recipes"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_account(cls,data):
        query = "INSERT INTO accounts (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM accounts;"
        results = connectToMySQL(cls.db).query_db(query)
        accounts = []
        for row in results:
            accounts.append( cls(row))
        return accounts

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM accounts WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM accounts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return None



    @staticmethod
    def validate_account(accounts):
        is_valid = True
        query = "SELECT * FROM accounts WHERE email = %(email)s;"
        results = connectToMySQL(accounts_class.db).query_db(query,accounts)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid = False
        if len(accounts['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(accounts['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(accounts['password']) < 3:
            flash("Password must be at least 3 characters.")
            is_valid = False
        if accounts['password'] != accounts['confirm']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid