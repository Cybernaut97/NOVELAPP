from flask import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


DATABASE = 'novel_app'

class Flavor:
    def __init__(self, data):
        self.id = data.get('id', None)
        self.name = data['name']
        self.description = data['description']
        self.is_ice_cream = data.get('is_ice_cream', True)

    @classmethod
    def update(cls, data):
        query = "UPDATE flavors SET name=%(name)s, description=%(description)s, is_ice_cream=%(is_ice_cream)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls,ice_cream_shop_id):
        query = "SELECT * FROM flavors"
        results = connectToMySQL(DATABASE).query_db(query)
        flavors = []
        for flavor in results:
            flavors.append(cls(flavor))
        return flavors
    
    @classmethod
    def save(cls, data=None):
        query = "INSERT INTO flavors (name, description, is_ice_cream) VALUES (%(name)s, %(description)s, %(is_ice_cream)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM flavors WHERE id = %(id)s"
        data = {'id': id}
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_ice_cream_flavors(cls):
        query = "SELECT * FROM flavors WHERE is_ice_cream = 1"
        results = connectToMySQL(DATABASE).query_db(query)
        ice_cream_flavors = []
        for flavor in results:
            ice_cream_flavors.append(cls(flavor))
        return ice_cream_flavors

    @classmethod
    def get_one_by_id(cls, id):
        query = "SELECT * FROM flavors WHERE id = %(id)s"
        data = {'id': id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
            return False
        else:
            flavor = cls(results[0])
        return flavor
    
    @classmethod
    def add_flavor_to_freezer(self, flavor_id, quantity):
        query = "INSERT INTO freezer_inventories (shop_id, flavor_id, quantity, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())"
        data = (self.id, flavor_id, quantity)
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def set_next_flavors(cls, shop_id, ice_cream_flavors, sorbet_flavors):
        # First, remove any existing next flavors for this shop
        query = "DELETE FROM shop_flavors WHERE shop_id = %s AND is_current = 0"
        data = (shop_id,)
        connectToMySQL(DATABASE).query_db(query, data)

        # Now set the new next flavors
        for i, flavor in enumerate(ice_cream_flavors[2:] + sorbet_flavors[2:]):
            query = "INSERT INTO shop_flavors (shop_id, flavor_id, is_current, position) VALUES (%s, %s, 0, %s)"
            data = (shop_id, flavor.id, i+1)
            connectToMySQL(DATABASE).query_db(query, data)

        for i, flavor in enumerate(ice_cream_flavors[2:] + sorbet_flavors[2:]):
            query = "INSERT INTO shop_flavors (shop_id, flavor_id, is_current, position) VALUES (%s, %s, 0, %s)"
            data = (shop_id, flavor.id, i+1)
            connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def set_next_flavors(cls, shop_id, ice_cream_flavors, sorbet_flavors):
    # First, remove any existing next flavors for this shop
        query = "DELETE FROM shop_flavors WHERE shop_id = %s AND is_current = 0"
        data = (shop_id,)
        connectToMySQL(DATABASE).query_db(query, data)

    # Now set the new next flavors
        for i, flavor in enumerate(ice_cream_flavors[2:] + sorbet_flavors[2:]):
            query = "INSERT INTO shop_flavors (shop_id, flavor_id, is_current, position) VALUES (%s, %s, 0, %s)"
            data = (shop_id, flavor.id, i+1)
        connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_sorbet_flavors(cls):
        query = "SELECT * FROM flavors WHERE is_ice_cream = 0"
        results = connectToMySQL(DATABASE).query_db(query)
        flavors = []
        for flavor in results:
            flavors.append(cls(flavor))
        return flavors

    @classmethod
    def set_current_flavors(cls, shop_id, ice_cream_flavors, sorbet_flavors):
        # First, remove any existing current flavors for this shop
        query = "UPDATE shop_flavors SET is_current = 0 WHERE shop_id = %s AND is_current = 1"
        data = (shop_id,)
        connectToMySQL(DATABASE).query_db(query, data)

        # Now set the new current flavors
        for i, flavor in enumerate(ice_cream_flavors[:2] + sorbet_flavors[:2]):
            query = "INSERT INTO shop_flavors (shop_id, flavor_id, is_current, position) VALUES (%s, %s, 1, %s)"
            data = (shop_id, flavor.id, i+1)
            connectToMySQL(DATABASE).query_db(query, data)        

    @staticmethod
    def is_valid(flavor):
        is_valid = True

        if not flavor['name']:
            flash ('Name is required', 'name')
            is_valid = False
        elif len(flavor['name']) < 2:
            flash('Name must be at least 2 characters')
            is_valid = False

        if not flavor['description']:
            flash ('Description is required', 'description')
            is_valid = False
        elif len(flavor['description']) < 10:
            flash('Description must be at least 10 characters')
            is_valid = False

        if not flavor['is_ice_cream']:
            flash ('Ice cream or sorbet selection is required', 'is_ice_cream')
            is_valid = False

        return is_valid
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_ice_cream': self.is_ice_cream
        }
    

    @classmethod
    def get_ice_cream_shop_id(cls, flavor_id):
        query = "SELECT ice_cream_shop_id FROM flavors WHERE id = %(id)s;"
        data = {'id': flavor_id}
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return None
        return result[0]['ice_cream_shop_id']