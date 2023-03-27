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

# @app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer', methods=['POST'])
# def add_to_freezer(ice_cream_shop_id):
#     user = User.get_one_by_id(int(session['id']))
#     ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
#     flavor_id = request.json.get('flavor_id')
#     flavor = Flavor.get_one_by_id(flavor_id)
#     quantity = request.json.get('quantity')

#     # Check if the ice cream shop exists
#     if not ice_cream_shop or ice_cream_shop.user_id != user.id:
#         return jsonify({'error': 'Ice cream shop not found'}), 404

#     # Check if the flavor already exists in the freezer
#     freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
#     if freezer_inventory:
#         freezer_inventory.quantity += int(quantity)
#         freezer_inventory.save()
#     else:
#         data = {
#             'shop_id': ice_cream_shop.id,
#             'flavor_id': flavor_id,
#             'quantity': quantity
#         }
#         FreezerInventory.save(data)

#     return jsonify({'success': f'{quantity} {flavor_id} added to the freezer at {ice_cream_shop.name}!'}), 200

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/freezer/remove_from_freezer', methods=['POST'])
def remove_from_freezer(ice_cream_shop_id):
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)

    data = request.get_json()
    print(f'Received data: {data}')

    if not data:
        return jsonify({'error': 'Missing data'}), 400
    if 'flavor_id' not in data or not isinstance(data['flavor_id'], int) or data['flavor_id'] <= 0:
        return jsonify({'error': 'Invalid flavor_id'}), 400
    if 'quantity' not in data or not isinstance(data['quantity'], int) or data['quantity'] <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400

    flavor_id = int(data['flavor_id'])
    quantity = data['quantity']

    freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
    print(f'Freezer inventory: {freezer_inventory}')
    if freezer_inventory:
        freezer_inventory.quantity -= int(quantity)
        print(f'New quantity: {freezer_inventory.quantity}')
        if freezer_inventory.quantity <= 0:
            freezer_inventory.delete()
            return jsonify({'success': 'Flavor removed from the freezer'})
        else:
            freezer_inventory.save()
            return jsonify({'success': f'Removed {quantity} from the freezer'})
    else:
        return jsonify({'error': 'Flavor not found in the freezer'}), 404




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


