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

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer', methods=['POST'])
def add_to_freezer(ice_cream_shop_id):
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    flavor_id = request.json.get('flavor_id')
    flavor = Flavor.get_one_by_id(flavor_id)
    quantity = request.json.get('quantity')

    # Check if the ice cream shop exists
    if not ice_cream_shop or ice_cream_shop.user_id != user.id:
        return jsonify({'error': 'Ice cream shop not found'}), 404

    # Check if the flavor already exists in the freezer
    freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
    if freezer_inventory:
        freezer_inventory.quantity += int(quantity)
        freezer_inventory.save()
    else:
        data = {
            'shop_id': ice_cream_shop.id,
            'flavor_id': flavor_id,
            'quantity': quantity
        }
        FreezerInventory.save(data)

    return jsonify({'success': f'{quantity} {flavor_id} added to the freezer at {ice_cream_shop.name}!'}), 200

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

# @app.route('/ice_cream_shops/<int:ice_cream_shop_id>/remove_from_freezer', methods=['POST'])
# def remove_from_freezer(ice_cream_shop_id):
#     user = User.get_one_by_id(int(session['id']))
#     ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)

#     data = request.get_json()

#     if not data:
#         return jsonify({'error': 'Missing data'}), 400
#     if 'flavor_id' not in data:
#         return jsonify({'error': 'Missing flavor_id'}), 400
#     if 'quantity' not in data:
#         return jsonify({'error': 'Missing quantity'}), 400

#     flavor_id = data['flavor_id']
#     quantity = data['quantity']

#     freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
#     if freezer_inventory:
#         freezer_inventory.quantity -= int(quantity)

#         if freezer_inventory.quantity <= 0:
#             freezer_inventory.delete()
#             return jsonify({'success': 'Flavor removed from the freezer'})
#         else:
#             freezer_inventory.save()
#             return jsonify({'success': f'Removed {quantity} from the freezer'})
#     else:
#         return jsonify({'error': 'Flavor not found in the freezer'}), 404
    
    
# @app.route('/freezer_inventories/<int:ice_cream_shop_id>/edit', methods=['GET'])
# def edit_freezer_inventory(inventory_id):
#     freezer_inventory = FreezerInventory.get_one_by_id(inventory_id)
#     return render_template('edit_freezer_inventory.html', freezer_inventory=freezer_inventory)


@app.route('/freezer_inventories/update/<int:inventory_id>', methods=['POST'])
def update_freezer_inventory(inventory_id):
    quantity = request.form['quantity']

    data = {
        'id': inventory_id,
        'quantity': quantity,
    }

    FreezerInventory.update(data)

    return redirect('/freezer_inventories')


@app.route('/freezer_inventories/<int:inventory_id>/delete', methods=['POST'])
def delete_freezer_inventory(inventory_id):
    FreezerInventory.delete(inventory_id)
    flash('Freezer inventory record deleted successfully!', 'success')

    return redirect('/freezer_inventories')


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


@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer', methods=['GET', 'POST'])
def add_to_freezer(ice_cream_shop_id):
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    flavor_id = request.args.get('flavor_id')  # Get the flavor_id from the request arguments.
    flavor = Flavor.get_one_by_id(flavor_id)  # Query the Flavor model to get the flavor object.

    if request.method == 'POST':
        data = request.get_json()

        print(f'Received data: {data}')

        if not data:
            return jsonify({'error': 'Missing data'}), 400
        if 'flavor_id' not in data:
            return jsonify({'error': 'Missing flavor_id'}), 400
        if 'quantity' not in data:
            return jsonify({'error': 'Missing quantity'}), 400

        else:
            quantity = request.json['quantity']
            flavor_id = request.json['flavor_id']

        # Check if the ice cream shop exists
        if not ice_cream_shop or ice_cream_shop.user_id != user.id:
            flash('Ice cream shop not found', 'error')
            return redirect(url_for('add_to_freezer'))

        # Check if the flavor already exists in the freezer
        freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
        if freezer_inventory:
            freezer_inventory.quantity += int(quantity)
            freezer_inventory.save()
        else:
            data = {
                'shop_id': ice_cream_shop_id,
                'flavor_id': flavor_id,
                'quantity': quantity
            }
            FreezerInventory.save(data)
            return jsonify({'success': 'Flavor added to the freezer'})
        flash(f'{quantity} {flavor.name} added to the freezer at {ice_cream_shop.name}!', 'success')
        return redirect(url_for('ice_cream_shops', ice_cream_shop_id=ice_cream_shop.id))

    return render_template('add_to_freezer.html', ice_cream_shop=ice_cream_shop, flavor=flavor)

# @app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer_submit', methods=['POST'])
# def add_to_freezer_submit(ice_cream_shop_id):
#     user = User.get_one_by_id(int(session['id']))
#     ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
#     flavor_id = request.args.get('flavor_id')  # Get the flavor_id from the request arguments.
#     flavor = Flavor.get_one_by_id(flavor_id)  # Query the Flavor model to get the flavor object.
#     print(f'Flavor object: {flavor}')
#     # Validate the form input
#     quantity = request.form['quantity']
#     flavor_id = request.form['flavor_id']
#     shop_id = request.form['shop_id']
    
#     # Check if the ice cream shop exists
#     ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
#     if not ice_cream_shop or ice_cream_shop.user_id != user.id:
#         flash('Ice cream shop not found', 'error')
#         return redirect(url_for('add_to_freezer'))

#     # Check if the flavor already exists in the freezer
#     freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
#     if freezer_inventory:
#         freezer_inventory.quantity += int(quantity)
#         freezer_inventory_data = {
#             'id': freezer_inventory.id,
#             'shop_id': freezer_inventory.shop_id,
#             'flavor_id': freezer_inventory.flavor_id,
#             'quantity': freezer_inventory.quantity
#         }
#         freezer_inventory.save(freezer_inventory_data)  # Pass the dictionary representation of the freezer_inventory object
#     else:
#         data = {
#             'shop_id': ice_cream_shop.id,
#             'flavor_id': flavor_id,
#             'quantity': quantity
#         }
#         FreezerInventory.save(data)
#     print(f'Flavor object: {flavor}')
#     if flavor:
#         flash(f'{quantity} {flavor.name} added to the freezer at {ice_cream_shop.name}!', 'success')
#     else:
#         flash('Flavor not found', 'error')
        
#     return redirect(url_for('dashboard', ice_cream_shop_id=ice_cream_shop.id))

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer_submit', methods=['POST'])
def add_to_freezer_submit(ice_cream_shop_id):
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)

    # Validate the form input
    quantity = request.form['quantity']
    flavor_id = request.form['flavor_id']

    # Check if flavor_id is not None before querying the database
    if flavor_id:
        flavor = Flavor.get_one_by_id(flavor_id)
    else:
        flavor = None

    # Check if the ice cream shop exists
    if not ice_cream_shop or ice_cream_shop.user_id != user.id:
        flash('Ice cream shop not found', 'error')
        return redirect(url_for('add_to_freezer'))

    # Check if the flavor already exists in the freezer
    freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
    if freezer_inventory:
        freezer_inventory.quantity += int(quantity)
        freezer_inventory.save({'quantity': freezer_inventory.quantity})
    else:
        data = {
        'shop_id': ice_cream_shop_id,
        'flavor_id': flavor_id,
        'quantity': quantity
        }
        FreezerInventory.save(data)

    if flavor:
        flash(f'{quantity} {flavor.name} added to the freezer at {ice_cream_shop.name}!', 'success')
    else:
        flash('Flavor not found', 'error')

    return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop.id))


@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/set_current', methods=['POST'])
def set_current_flavor(ice_cream_shop_id):
    inventory = FreezerInventory.get_one_by_id(ice_cream_shop_id)
    if inventory:
        inventory.current_flavor = True
        inventory.quantity -= 1
        inventory.save({'current_flavor': inventory.current_flavor, 'quantity': inventory.quantity})
        message = f'{inventory.flavor.name} set as current flavor and removed 1 from the quantity!'
        return jsonify({"status": "success", "message": message})
    else:
        return jsonify({"status": "error", "message": "Inventory item not found"})