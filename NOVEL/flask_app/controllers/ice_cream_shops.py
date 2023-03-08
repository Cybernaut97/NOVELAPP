
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.freezer_inventory import FreezerInventory
from flask_app.models.flavor import Flavor

DATABASE = 'novel_app'


@app.route('/ice_cream_shops')
def ice_cream_shops():
    ice_cream_shops = IceCreamShop.get_all()
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
        'phone_number': request.form['phone_number']
    }
    IceCreamShop.save(data)
    flash('New ice cream shop created!')
    return redirect('/ice_cream_shops')

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>')
def show_ice_cream_shop(ice_cream_shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    return render_template('show_ice_cream_shop.html', ice_cream_shop=ice_cream_shop)


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

# @app.route('/ice_cream_shops/<int:shop_id>/assign_user')
# def assign_user(shop_id):
#     ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
#     users = User.get_all()
#     return render_template('assign_user_to_shop.html', ice_cream_shop=ice_cream_shop, users=users)

@app.route('/ice_cream_shops/<int:shop_id>/assign_user', methods=['GET', 'POST'])
def assign_user(shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
    users = User.get_all()
    if request.method == 'POST':
        user_id = request.form['user_id']
        # assign the user to the shop here
        flash('User assigned to shop!', 'success')
        return redirect('/ice_cream_shops')
    else:
        return render_template('assign_user_to_shop.html', ice_cream_shop=ice_cream_shop, users=users)

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/freezer')
def freezer(ice_cream_shop_id):
    inventory = FreezerInventory.get_all_by_shop_id(ice_cream_shop_id)
    if not inventory:
        flash('No inventory found for this ice cream shop', 'error')
        return redirect('/ice_cream_shops')

    items = []
    for item in inventory:
        flavor = Flavor.get_one_by_id(item.flavor_id)
        if flavor:
            items.append({
                'name': flavor.name,
                'quantity': item.quantity
            })

    return render_template('freezer.html', shop_id=ice_cream_shop_id, items=items)

@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/freezer/add/<int:flavor_id>', methods=['GET', 'POST'])
def add_to_freezer(ice_cream_shop_id, flavor_id):
    ice_cream_shop = IceCreamShop.get_one_by_id({'id': ice_cream_shop_id})
    if request.method == 'POST':
        ice_cream_shop_id = request.form['shop_id']
        flavor_id = request.form['flavor_id']
        quantity = request.form['quantity']
        freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop_id, flavor_id)
        if freezer_inventory:
            data = {
                'shop_id': ice_cream_shop_id,
                'flavor_id': flavor_id,
                'quantity': freezer_inventory.quantity + int(quantity)
            }
            FreezerInventory.update(data)
        else:
            data = {
                'shop_id': ice_cream_shop_id,
                'flavor_id': flavor_id,
                'quantity': quantity
            }
            FreezerInventory.save(data)
        flash('Flavor added to freezer successfully!', 'success')
        return redirect(url_for('freezer', ice_cream_shop_id=ice_cream_shop_id))
    else:
        ice_cream_flavor = Flavor.get_one_by_id({'id': flavor_id})
        return render_template('add_to_freezer.html', ice_cream_shop=ice_cream_shop, ice_cream_flavor=ice_cream_flavor, shop_id=shop_id)
        ice_cream_flavors = Flavor.get_all()
        print(f"shop_id in render_template: {shop_id}")
        return render_template('add_to_freezer.html', ice_cream_shop=ice_cream_shop, ice_cream_flavors=ice_cream_flavors, shop_id=shop_id)