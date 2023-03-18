from flask import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.flavor import Flavor
from flask_app.models.ice_cream_shop import IceCreamShop

DATABASE = 'novel_app'

class FreezerInventory:
    def __init__(self, data):
        self.id = data['id']
        self.shop_id = data['shop_id']
        self.flavor_id = data['flavor_id']
        self.current_flavor = data['current_flavor']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO freezer_inventories (shop_id, flavor_id, current_flavor, quantity, created_at, updated_at) VALUES (%(shop_id)s, %(flavor_id)s, %(current_flavor)s, %(quantity)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM freezer_inventories"
        results = connectToMySQL(DATABASE).query_db(query)
        inventories = []
        for inventory in results:
            inventories.append(cls(inventory))
        return inventories
    
    @classmethod
    def get_all_by_shop_id(cls, shop_id):
        query = "SELECT * FROM freezer_inventories WHERE shop_id = %(shop_id)s"
        data = {'shop_id': shop_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        inventories = []
        for inventory in results:
            inventories.append(cls(inventory))
        return inventories

    @classmethod
    def get_by_shop_and_flavor(cls, shop_id, flavor_id):
        query = "SELECT * FROM freezer_inventories WHERE shop_id = %(shop_id)s AND flavor_id = %(flavor_id)s"
        data = {'shop_id': shop_id, 'flavor_id': flavor_id}
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) == 0:
            return None
        else:
            return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE freezer_inventories SET current_flavor = %(current_flavor)s, quantity = %(quantity)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM freezer_inventories WHERE id = %(id)s"
        data = {'id': id}
        return connectToMySQL(DATABASE).query_db(query, data)