from flask_app import app
from flask_login import current_user
from flask import jsonify
from flask_app import AUTHORIZED_USER_IDS
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


@app.route('/inventory')
def inventory():
    if 'user_id' not in session:
        flash("You must be logged in to access this page!", "error")
        return redirect('/')

    inventories = FreezerInventory.get_all()
    ice_cream_shops = IceCreamShop.get_all()

    ice_cream_shops = IceCreamShop.get_all()
    shop_dict = {shop.id: shop for shop in ice_cream_shops}
    
    shop_inventory = {}
    for inventory in inventories:
        if inventory.shop_id not in shop_inventory:
            shop_inventory[inventory.shop_id] = []
        shop_inventory[inventory.shop_id].append(inventory)

    return render_template('inventory.html', all_inventory=inventories, ice_cream_shops=ice_cream_shops, shop_inventory=shop_inventory, shop_dict=shop_dict)





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

