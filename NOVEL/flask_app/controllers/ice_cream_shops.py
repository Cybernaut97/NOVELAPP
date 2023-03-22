
from flask_app import app
from flask_login import current_user
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.freezer_inventory import FreezerInventory
from flask_app.models.flavor import Flavor
from flask import jsonify
import json
DATABASE = 'novel_app'


@app.route('/ice_cream_shops')
def ice_cream_shops():
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shops = IceCreamShop.get_all()
    print(ice_cream_shops)  # print to console
    return render_template('ice_cream_shop.html', ice_cream_shops=ice_cream_shops)

@app.route('/ice_cream_shops/new', methods=['GET'])
def new_ice_cream_shop():
    print('new_ice_cream_shop() function called')
    return render_template('add_ice_cream_shop.html')

@app.route('/ice_cream_shops/create', methods=['POST'])
def create_ice_cream_shop():
    if not IceCreamShop.is_valid(request.form):
        return redirect('/ice_cream_shops/new')

    data = {
        'name': request.form['name'],
        'address': request.form['address'],
        'phone_number': request.form['phone_number'],
        'user_id': session['id']
    }
    IceCreamShop.save(data)
    flash('New ice cream shop created!')
    return redirect('/ice_cream_shops')

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>')
def show_ice_cream_shop(ice_cream_shop_id):
    # Retrieve the ice cream shop object from the database
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)

    # Retrieve the list of flavors available at the ice cream shop
    flavors = Flavor.get_one_by_id(ice_cream_shop_id)

    # Retrieve the freezer inventory for the ice cream shop
    freezer_inventory = FreezerInventory.get_all_by_shop_id(ice_cream_shop_id)

    # Render the template with the retrieved data
    return render_template('freezer.html', ice_cream_shop=ice_cream_shop, flavors=flavors, freezer_inventory=freezer_inventory)

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/edit', methods=['GET'])
def edit_ice_cream_shop(ice_cream_shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    return render_template('edit_ice_cream_shop.html', ice_cream_shop=ice_cream_shop)

@app.route('/ice_cream_shops/update/<int:ice_cream_shop_id>', methods=['POST'])
def update_ice_cream_shop(ice_cream_shop_id):
    name = request.form['name']
    address = request.form['address']
    phone_number = request.form['phone_number']

    data = {
        'id': ice_cream_shop_id,
        'name': name,
        'address': address,
        'phone_number': phone_number,
    }

    IceCreamShop.update(data)

    return redirect('/ice_cream_shops?id=' + str(ice_cream_shop_id))


@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/delete', methods=['POST'])
def delete_ice_cream_shop(ice_cream_shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    if ice_cream_shop is None:
        flash('Ice cream shop not found', 'error')
        return redirect('/ice_cream_shops')
    
    if request.form.get(f'confirm_delete_{ice_cream_shop_id}') == 'yes':
        IceCreamShop.delete(ice_cream_shop_id)
        flash('Ice cream shop deleted successfully!', 'success')
    else:
        flash('Deletion canceled', 'info')
    
    return redirect('/ice_cream_shops')

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/freezer', methods=['GET', 'POST'])
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
            print(f"Flavor ID: {item.flavor_id} Flavor Name: {flavor.name}")  # added print statement
            items.append(item_data)

    if request.method == 'POST':
        flavor_id = request.form['flavor_id']
        action = request.form['action']
        return update_freezer(ice_cream_shop_id, flavor_id, action)

    return render_template('freezer.html', ice_cream_shop=ice_cream_shop, items=items)


@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer/<int:flavor_id>', methods=['GET', 'POST'])
def add_to_freezer(ice_cream_shop_id, flavor_id):
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    flavor = Flavor.get_one_by_id(flavor_id)

    if request.method == 'POST':
        quantity = request.form.get('quantity')
        
        if flavor_id and quantity:
            freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop_id, flavor_id)
            if freezer_inventory:
                freezer_inventory.quantity += int(quantity)
                # freezer_inventory.save(data=None)  # Pass data=None as an argument
            else:
                data = {
                    'shop_id': ice_cream_shop_id,
                    'flavor_id': flavor_id,
                    'quantity': quantity
                }
                FreezerInventory.save(data)

            flash(f'{quantity} pans of {Flavor.get_one_by_id(flavor_id).name} have been added to the freezer at {ice_cream_shop.name}.', 'success')
            return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop_id))
        else:
            flash('Please select a flavor and specify a quantity.', 'error')

    return render_template('add_to_freezer.html', ice_cream_shop=ice_cream_shop, flavor=flavor)

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer_submit', methods=['POST'])
def add_to_freezer_submit(ice_cream_shop_id):
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    flavor_id = request.args.get('flavor_id')
    quantity = request.form.get('quantity')
    
    if not flavor_id:
        flash('No flavor selected', 'error')
        return redirect(url_for('add_to_freezer', ice_cream_shop_id=ice_cream_shop_id))
    
    freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop_id, flavor_id)
    if freezer_inventory:
        freezer_inventory.quantity += int(quantity)
        freezer_inventory.save()
        flash(f'{quantity} added to the freezer inventory for {ice_cream_shop.name}!', 'success')
    else:
        data = {
            'shop_id': ice_cream_shop_id,
            'flavor_id': flavor_id,
            'quantity': quantity
        }
        FreezerInventory.save(data)
        flash(f'{quantity} added to the freezer inventory for {ice_cream_shop.name}!', 'success')
    
    return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop_id))


@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/update_freezer', methods=['POST'])
def update_freezer(ice_cream_shop_id):
    flavor_id = int(request.form['flavor_id'])
    action = request.form['action']
    print(f"Flavor ID: {flavor_id}")  # added print statement

    inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop_id, flavor_id)
    if not inventory:
        flash('No inventory found for this ice cream shop and flavor', 'error')
        return redirect('/ice_cream_shops')

    if action == 'add':
        inventory.quantity += 1
        inventory.current_flavor = True
        inventory.save()
        flash(f'Added 1 unit of flavor {inventory.flavor.name} to the freezer inventory', 'success')
    elif action == 'remove':
        if inventory.quantity > 0:
            inventory.quantity -= 1
            inventory.save()
            flash(f'Removed 1 unit of flavor {inventory.flavor.name} from the freezer inventory', 'success')
        else:
            flash('Cannot remove more units, inventory is already empty', 'error')
    elif action == 'make_current':
        inventory.current_flavor = True
        inventory.save()
        flash(f'{inventory.flavor.name} is now the current flavor in the freezer inventory', 'success')

    return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop_id))




@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/make_current/<int:flavor_id>', methods=['POST'])
def make_current(ice_cream_shop_id, flavor_id):
    # Print statements for debugging
    print(f"ice_cream_shop_id: {ice_cream_shop_id}")
    print(f"flavor_id: {flavor_id}")
    inventory_items = FreezerInventory.get_all_by_shop_id(ice_cream_shop_id)
    for item in inventory_items:
        print(f"Inventory item flavor_id: {item.flavor_id}")

    # Update is_current to 1 for the specified flavor in the ice cream shop's freezer inventory
    inventory_item = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop_id, flavor_id)
    if inventory_item:
        inventory_item.is_current = 1
        inventory_item.quantity -= 1
        FreezerInventory.update({'id': inventory_item.id, 'quantity': inventory_item.quantity})
        flash(f"{Flavor.get_one_by_id(flavor_id).name} has been set as the current flavor!", 'success')
    else:
        flash('Freezer inventory not found.', 'error')

    return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop_id))


# @app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer_submit', methods=['POST'])
# def add_to_freezer_submit(ice_cream_shop_id):
#     user = User.get_one_by_id(int(session['id']))
#     ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)

#     # Validate the form input
#     quantity = request.form['quantity']
#     flavor_id = request.form['flavor_id']

#     # Check if flavor_id is not None before querying the database
#     if flavor_id:
#         flavor = Flavor.get_one_by_id(flavor_id)
#     else:
#         flavor = None

#     # Check if the ice cream shop exists
#     if not ice_cream_shop or ice_cream_shop.user_id != user.id:
#         flash('Ice cream shop not found', 'error')
#         return redirect(url_for('add_to_freezer'))

#     # Check if the flavor already exists in the freezer
#     freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
#     if freezer_inventory:
#         freezer_inventory.quantity += int(quantity)
#         freezer_inventory.save({'quantity': freezer_inventory.quantity})
#     else:
#         data = {
#         'shop_id': ice_cream_shop_id,
#         'flavor_id': flavor_id,
#         'quantity': quantity
#         }
#         FreezerInventory.save(data)

#     if flavor:
#         flash(f'{quantity} {flavor.name} added to the freezer at {ice_cream_shop.name}!', 'success')
#     elif flavor_id:
#         flash('Flavor not found', 'error')
#     else:
#         flash('No flavor selected', 'error')

#     return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop.id))