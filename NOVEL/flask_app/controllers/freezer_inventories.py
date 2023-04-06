from flask_app import app
from flask_login import current_user
from flask import jsonify

from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.freezer_inventory import FreezerInventory
from flask_app.models.flavor import Flavor

DATABASE = 'novel_app'



@app.route('/freezer_inventories')
def freezer_inventories():
    user = User.get_one_by_id(int(session['id']))
    freezer_inventories = FreezerInventory.get_all()
    return render_template('freezer_inventory.html', freezer_inventories=freezer_inventories)

from flask import jsonify


@app.route('/freezer_inventories/<int:inventory_id>/delete', methods=['POST'])
def delete_freezer_inventory(inventory_id):
    FreezerInventory.delete(inventory_id)
    flash('Freezer inventory record deleted successfully!', 'success')

    return redirect('/freezer_inventories')

@classmethod
def get_one_by_shop_and_flavor(cls, shop_id, flavor_id):
    query = "SELECT * FROM freezer_inventories WHERE shop_id=%(shop_id)s AND flavor_id=%(flavor_id)s;"
    data = {'shop_id': shop_id, 'flavor_id': flavor_id}
    result = connectToMySQL(DATABASE).query_db(query, data)
    if result:
        return cls(result[0])
    return None

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/freezer')
def freezer(ice_cream_shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    inventory = FreezerInventory.get_all_by_shop_id(ice_cream_shop_id)
    if not inventory:
        flash('No inventory found for this ice cream shop', 'error')
        return redirect('/ice_cream_shops')

    items = []
    for item in inventory:
        flavor = Flavor.get_one_by_id(item.flavor_id)
        if flavor:
            item_data = {
            'id': item.id,
            'name': flavor.name,
            'quantity': item.quantity
            }
            print(f"Flavor: {item_data['name']}, Quantity: {item_data['quantity']}")
            items.append(item_data)
    

    return render_template('freezer.html', ice_cream_shop=ice_cream_shop, items=items)


