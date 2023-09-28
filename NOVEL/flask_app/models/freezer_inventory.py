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
        self.current_flavor = data.get('current_flavor', False) 
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.flavor = Flavor.get_one_by_id(self.flavor_id)
        self.shop = IceCreamShop.get_one_by_id(self.shop_id)

    def save(self):
        data = {
            'shop_id': self.shop_id,
            'flavor_id': self.flavor_id,
            'quantity': self.quantity,
            'current_flavor': self.current_flavor, 
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        if self.id:
            if self.quantity == 0:
                # Delete the record
                query = "DELETE FROM freezer_inventories WHERE id=%(id)s;"
            else:
                # Update the record
                data['id'] = self.id
                query = "UPDATE freezer_inventories SET shop_id=%(shop_id)s, flavor_id=%(flavor_id)s, quantity=%(quantity)s, current_flavor=%(current_flavor)s, updated_at=NOW() WHERE id=%(id)s;"
        else:
            # Insert a new record
            query = "INSERT INTO freezer_inventories (shop_id, flavor_id, quantity, current_flavor, created_at, updated_at) VALUES (%(shop_id)s, %(flavor_id)s, %(quantity)s, %(current_flavor)s, NOW(), NOW());"

        connectToMySQL(DATABASE).query_db(query, data)

    def make_current(self):
        self.current_flavor = True
        self.save()

    def remove_current(self):
        self.current_flavor = False
        self.save()

    @classmethod
    def delete_by_flavor_id(cls, flavor_id):
        query = "DELETE FROM freezer_inventories WHERE flavor_id=%(flavor_id)s;"
        data = {'flavor_id': flavor_id}
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