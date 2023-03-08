from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'novel_app'
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.shop_id = data['shop_id'] # added field
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def update(self):
        query = "UPDATE users SET shop_id = %(shop_id)s WHERE id = %(id)s;"
        data = {
            'shop_id': self.shop_id,
            'id': self.id
        }
        connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,shop_id) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(shop_id)s)"
        return connectToMySQL(DATABASE).query_db(query,data)
        
    # rest of the methods remain unchanged

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users


    @classmethod
    def get_one_by_email(cls,email):
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {'email':email}
        result = connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return result
        return cls(result[0])

    @classmethod
    def get_one_by_id(cls,id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id':id}
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    @staticmethod
    def is_valid(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash('Email not in valid format')
            is_valid = False
        all_users = User.get_all()
        for user in all_users:
            if (user.email == data['email']):
                flash('Email already in use!')
                is_valid = False
        if (len(data['first_name']) < 2) or not data['first_name'].isalpha():
            flash('First name must be at least two characters')
            is_valid = False
        if (len(data['last_name']) < 2) or not data['last_name'].isalpha():
            flash('Last name must be at least two characters')
            is_valid = False
        if not data['password'] == data['password2']:
            flash('Passwords do not match')
            is_valid = False
        if (len(data['password']) < 8):
            flash('Password must be at least 8 characters')
            is_valid = False
        if is_valid:
            flash('User Created')
        return is_valid

    @staticmethod
    def newUser(data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query,data)