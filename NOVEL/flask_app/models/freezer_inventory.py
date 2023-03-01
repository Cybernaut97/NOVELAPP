import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


DATABASE = 'novel_app'
class FreezerInventory:
    def __init__(self, data):
        self.id = data['id']
        self.shop_id = data['shop_id']
        self.flavor_id = data['flavor_id']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_one_by_id(cls, freezer_id):
        query = "SELECT * FROM freezer_inventories WHERE id = %(id)s;"
        data = {'id': freezer_id}
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    @staticmethod
    def get_one_by_shop_id_and_flavor_id(shop_id, flavor_id):
        query = "SELECT * FROM freezer_inventories WHERE shop_id = %(shop_id)s AND flavor_id = %(flavor_id)s;"
        data = {
        "shop_id": shop_id,
        "flavor_id": flavor_id
    }
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
        # If a result is found, return the first item in the list
            return cls(result[0])
        else:
        # If no result is found, return None
            return None
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM freezer_inventories;"
        results = connectToMySQL(DATABASE).query_db(query)
        freezers = []
        for freezer in results:
            freezers.append(cls(freezer))
        return freezers
    
    def save(self):
        if self.id is None:
            query = "INSERT INTO freezer_inventories (shop_id, flavor_id, quantity) VALUES (%(shop_id)s, %(flavor_id)s, %(quantity)s);"
            data = {'shop_id': self.shop_id, 'flavor_id': self.flavor_id, 'quantity': self.quantity}
            self.id = connectToMySQL(DATABASE).query_db(query, data)
        else:
            query = "UPDATE freezer_inventories SET shop_id = %(shop_id)s, flavor_id = %(flavor_id)s, quantity = %(quantity)s WHERE id = %(id)s;"
            data = {'shop_id': self.shop_id, 'flavor_id': self.flavor_id, 'quantity': self.quantity, 'id': self.id}
            connectToMySQL(DATABASE).query_db(query, data)
    
    def delete(self):
        query = "DELETE FROM freezer_inventories WHERE id = %(id)s;"
        data = {'id': self.id}
        connectToMySQL(DATABASE).query_db(query, data)
        self.id = None