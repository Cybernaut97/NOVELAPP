from flask import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.flavor import Flavor
from flask_app.models.ice_cream_shop import IceCreamShop

DATABASE = 'novel_app'

class FreezerInventory:
    def __init__(self, data):
        self.id = data.get('id')
        self.shop_id = data.get('shop_id')
        self.flavor_id = data.get('flavor_id')
        self.quantity = data.get('quantity', 0)
        # self.current_flavor = data.get('current_flavor', False)  # Add this line
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.flavor = Flavor.get_one_by_id(self.flavor_id)

    @classmethod
    def save(cls, data):
        freezer_inventory = cls.get_by_shop_and_flavor(data['shop_id'], data['flavor_id'])
        if freezer_inventory:
            data['id'] = freezer_inventory.id
            data['quantity'] = freezer_inventory.quantity + int(data['quantity'])
            return cls.update(data)
        else:
            query = "INSERT INTO freezer_inventories (shop_id, flavor_id, quantity, created_at, updated_at) VALUES (%(shop_id)s, %(flavor_id)s, %(quantity)s, NOW(), NOW());"
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
        query = "UPDATE freezer_inventories SET quantity = %(quantity)s, updated_at = NOW() WHERE id = %(id)s AND flavor_id = %(flavor_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM freezer_inventories WHERE id = %(id)s"
        data = {'id': id}
        return connectToMySQL(DATABASE).query_db(query, data)