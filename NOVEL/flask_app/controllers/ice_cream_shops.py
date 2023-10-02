from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app import AUTHORIZED_USER_IDS
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


@app.route('/api/ice_cream_shops')
def api_ice_cream_shops():
    ice_cream_shops = IceCreamShop.get_all()
    shop_data = []
    for shop in ice_cream_shops:
        flavors = shop.get_current_flavors()
        shop_data.append({
            'name': shop.name,
            'address': shop.address,
            'phone_number': shop.phone_number,
            'current_flavors': [
                {'name': flavor.name, 'description': flavor.description} for flavor in flavors['ice_cream_flavors'] + flavors['sorbet_flavors']
            ]
        })
    return jsonify(shop_data)


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
    user = User.get_one_by_id(int(session['id']))
    if not IceCreamShop.is_valid(request.form):
        return redirect('/ice_cream_shops/new')

    data = {
        'name': request.form['name'],
        'address': request.form['address'],
        'phone_number': request.form['phone_number'],
        'user_id': session['id'],
        'square_location_id': request.form.get('square_location_id')  # New line
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


@app.route("/ice_cream_shops/<int:shop_id>/assign_user", methods=["POST"])
def assign_user_to_shop(shop_id):
    form_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['user_password'],
    }

    if not User.is_valid(form_data):
        return redirect(f"/ice_cream_shops/{shop_id}/edit")

    pw_hash = bcrypt.generate_password_hash(request.form['user_password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    user_id = User.newUser(data)
    
    IceCreamShop.assign_user(shop_id, user_id)
    
    flash("User successfully assigned", "success")
    return redirect(f"/ice_cream_shops/{shop_id}/edit")

@app.route('/ice_cream_shops/<int:shop_id>/remove_user', methods=['POST'])
def remove_user_from_shop(shop_id):
    IceCreamShop.remove_user(shop_id)
    flash("User successfully removed", "success")
    return redirect(f"/ice_cream_shops/{shop_id}/edit")


@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/delete', methods=['POST'])
def delete_ice_cream_shop(ice_cream_shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    if ice_cream_shop is None:
        flash('Ice cream shop not found', 'error')
        return redirect('/ice_cream_shops')
    
    if request.form.get(f'confirm_delete_{ice_cream_shop_id}') == 'yes':
        IceCreamShop.delete(ice_cream_shop_id)
        FreezerInventory.delete(ice_cream_shop_id)
        flash('Ice cream shop deleted successfully!', 'success')
    else:
        flash('Deletion canceled', 'info')
    
    return redirect('/ice_cream_shops')

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/freezer', methods=['GET', 'POST'])
def freezer(ice_cream_shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    inventory = FreezerInventory.get_all_by_shop_id(ice_cream_shop_id)
    if not inventory:
        flash('No ice cream found for this ice cream shop, go to flavor page and add to inventory', 'error')
        return redirect('/ice_cream_shops')

    items = []
    for item in inventory:
        flavor = Flavor.get_one_by_id(item.flavor_id)
        if flavor:
            item_data = {
            'flavor_id': item.flavor_id, 
            'name': flavor.name,
            'quantity': item.quantity,
            'is_current': item.current_flavor
            }
            items.append(item_data)

    if request.method == 'POST':
        flavor_id = request.form['flavor_id']
        action = request.form['action']
        return update_freezer(ice_cream_shop_id, flavor_id, action)

    current_flavors = ice_cream_shop.get_current_flavors()
    sorted_items = sorted(items, key=lambda x: x['is_current'], reverse=True)

    return render_template('freezer.html', ice_cream_shop=ice_cream_shop, items=sorted_items, ice_cream_shop_id=ice_cream_shop_id, ice_cream_flavors=current_flavors['ice_cream_flavors'], sorbet_flavors=current_flavors['sorbet_flavors'])


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
                freezer_inventory.save()
            else:
                data = {
                    'shop_id': ice_cream_shop_id,
                    'flavor_id': flavor_id,
                    'quantity': quantity
                }
                new_inventory = FreezerInventory(data)  # Create a new instance of FreezerInventory
                new_inventory.save()  # Call save() method on the instance

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

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/update_freezer/<int:flavor_id>', methods=['POST'])
def update_freezer(ice_cream_shop_id, flavor_id, action=None):
    user = User.get_one_by_id(int(session['id'])) 
    flavor_id = int(request.form['flavor_id'])
    action = request.form['action']

    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)

    if user.id != ice_cream_shop.user_id:
        flash(' Not allowed, not your shop', 'error')
        return redirect('/ice_cream_shops')
    
    print(f"Flavor ID: {flavor_id}")  # added print statement

    inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop_id, flavor_id)
    if not inventory:
        flash('No inventory found for this ice cream shop and flavor', 'error')
        return redirect('/ice_cream_shops')

    if action == 'add':
        inventory.quantity += 1
        # inventory.current_flavor = True
        inventory.save()
        flash(f'Added 1 pan of {inventory.flavor.name} to the freezer inventory', 'success')
    elif action == 'remove':
        if inventory.quantity > 0:
            inventory.quantity -= 1
            if inventory.quantity == 0:
                # Remove the inventory record from the database
                FreezerInventory.delete_by_flavor_id(flavor_id)
                flash(f'Removed the last pan of {inventory.flavor.name} from the freezer inventory ', 'success')
            else:
                inventory.save()
                flash(f'Removed 1 pan of  {inventory.flavor.name} from the freezer inventory', 'success')
        else:
            flash('Cannot remove more pans, inventory is already empty', 'error')
    elif action == 'make_current':
        inventory.make_current()
        flash(f'{inventory.flavor.name} was added to Current Flavor List', 'success')
    elif action == 'remove_current':
        inventory.remove_current()
        flash(f'{inventory.flavor.name} was removed as current flavor', 'success')

    return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop_id))


@app.route('/shops/<int:ice_cream_shop_id>/flavors/<int:flavor_id>/remove_current', methods=['POST'])
def remove_flavor_from_current(ice_cream_shop_id, flavor_id):
    inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop_id, flavor_id)
    if inventory:
        inventory.remove_current()
        flash(f'{inventory.flavor.name} has been removed from the current flavors', 'success')
    else:
        flash('Error: Inventory not found', 'danger')
    return redirect(url_for('dashboard'))


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
