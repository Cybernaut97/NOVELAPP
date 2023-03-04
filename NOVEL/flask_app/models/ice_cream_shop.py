import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


DATABASE = 'novel_app'
class IceCreamShop:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.address = data['address']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ice_cream_shops"
        results = connectToMySQL(DATABASE).query_db(query)
        shops = []
        for shop in results:
            shops.append(cls(shop))
        return shops
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO ice_cream_shops (name, address, phone_number, created_at, updated_at) VALUES (%(name)s, %(address)s, %(phone_number)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM ice_cream_shops WHERE id = %(id)s"
        data = {'id': id}
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE ice_cream_shops SET name = %(name)s, address = %(address)s, phone_number = %(phone_number)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE ice_cream_shops SET name = %(name)s, address = %(address)s, phone_number = %(phone_number)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one_by_id(cls, id):
        query = "SELECT * FROM ice_cream_shops WHERE id = %(id)s"
        data = {'id': id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
            return False
        else:
            shop = cls(results[0])
        return cls(results[0])

    @staticmethod
    def is_valid(shop):
        is_valid = True

        if not shop['name']:
            flash ('Name is required', 'name')
            is_valid = False
        elif len(shop['name']) < 2:
            flash ('Name must be at least 2 characters', 'name')
            is_valid = False

        if not shop['address']:
            flash ('Address is required', 'address')
            is_valid = False

        if not shop['phone_number']:
            flash ('Phone number is required', 'phone_number')
            is_valid = False

        return is_valid

    def get_current_flavors(self):
        query = "SELECT flavors.id, flavors.name, flavors.description FROM flavors INNER JOIN shop_flavors ON flavors.id = shop_flavors.flavor_id WHERE shop_flavors.shop_id = %(shop_id)s AND shop_flavors.is_current = 1 AND shop_flavors.is_ice_cream = 1 LIMIT 2;"

        data = {'shop_id': self.id}

        results = connectToMySQL(DATABASE).query_db(query, data)

        ice_cream_flavors = []

        for flavor in results:
            ice_cream_flavors.append(Flavor(flavor))

        query = "SELECT flavors.id, flavors.name, flavors.description FROM flavors INNER JOIN shop_flavors ON flavors.id = shop_flavors.flavor_id WHERE shop_flavors.shop_id = %(shop_id)s AND shop_flavors.is_current = 1 AND shop_flavors.is_ice_cream = 0 LIMIT 2;"

        data = {'shop_id': self.id}

        results = connectToMySQL(DATABASE).query_db(query, data)

        sorbet_flavors = []

        for flavor in results:
            sorbet_flavors.append(Flavor(flavor))

        return {'ice_cream_flavors': ice_cream_flavors, 'sorbet_flavors': sorbet_flavors}

    def get_next_flavors(self):
        query = "SELECT flavors.id, flavors.name, flavors.description FROM flavors INNER JOIN shop_flavors ON flavors.id = shop_flavors.flavor_id WHERE shop_flavors.shop_id = %(shop_id)s AND shop_flavors.is_current = 0 AND shop_flavors.is_ice_cream = 1 LIMIT 2;"

        data = {'shop_id': self.id}

        results = connectToMySQL(DATABASE).query_db(query, data)

        ice_cream_flavors = []

        for flavor in results:
            ice_cream_flavors.append(Flavor(flavor))

        query = "SELECT flavors.id, flavors.name, flavors.description FROM flavors INNER JOIN shop_flavors ON flavors.id = shop_flavors.flavor_id WHERE shop_flavors.shop_id = %(shop_id)s AND shop_flavors.is_current = 0 AND shop_flavors.is_ice_cream = 0 LIMIT 2;"

        data = {'shop_id': self.id}

        results = connectToMySQL(DATABASE).query_db(query, data)

        sorbet_flavors = []

        for flavor in results:
            sorbet_flavors.append(Flavor(flavor))

        return {'ice_cream_flavors': ice_cream_flavors, 'sorbet_flavors': sorbet_flavors}