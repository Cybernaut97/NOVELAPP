
from flask_app import app
from flask_login import current_user
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.freezer_inventory import FreezerInventory
from flask_app.models.flavor import Flavor

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
    flavors = Flavor.get_all_by_shop_id(ice_cream_shop_id)

    # Retrieve the freezer inventory for the ice cream shop
    freezer_inventory = FreezerInventory.get_all_by_shop_id(ice_cream_shop_id)

    # Render the template with the retrieved data
    return render_template('view_shop.html', ice_cream_shop=ice_cream_shop, flavors=flavors, freezer_inventory=freezer_inventory)


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
    
@app.route('/ice_cream_shops/<int:shop_id>/check_user_assignment/<int:user_id>', methods=['GET'])
def check_user_assignment(shop_id, user_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
    user = User.get_one_by_id(user_id)

    if user in ice_cream_shop.users:
        message = f'{user.first_name} is assigned to {ice_cream_shop.name}'
    else:
        message = f'{user.first_name} is not assigned to {ice_cream_shop.name}'

    return render_template('check_user_assignment.html', message=message)

@app.route('/ice_cream_shops/<int:shop_id>/freezer')
def freezer(shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
    inventory = FreezerInventory.get_all_by_shop_id(shop_id)
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

    return render_template('freezer.html', ice_cream_shop=ice_cream_shop, items=items)


@app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer')
def add_to_freezer(ice_cream_shop_id):
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    flavors = Flavor.get_all()
    return render_template('add_to_freezer.html', ice_cream_shop=ice_cream_shop, flavors=flavors)

# @app.route('/ice_cream_shops/<int:ice_cream_shop_id>/add_to_freezer', methods=['POST'])
# def add_flavor_to_freezer():
#     user = User.get_one_by_id(int(session['id']))
#     ice_cream_shops = IceCreamShop.get_by_user(user.id)

#     if request.method == 'POST':
#         # Validate the form input
#         name = request.form['name']
#         quantity = request.form['quantity']
#         flavor_id = request.form['flavor_id']
#         shop_id = request.form['shop_id']
        
#         # Check if the ice cream shop exists
#         ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
#         if not ice_cream_shop or ice_cream_shop.user_id != user.id:
#             flash('Ice cream shop not found', 'error')
#             return redirect(url_for('add_flavor_to_freezer'))

#         # Check if the flavor already exists in the freezer
#         freezer_inventory = FreezerInventory.get_by_shop_and_flavor(ice_cream_shop.id, flavor_id)
#         if freezer_inventory:
#             freezer_inventory.quantity += int(quantity)
#             freezer_inventory.save()
#         else:
#             data = {
#                 'shop_id': ice_cream_shop.id,
#                 'flavor_id': flavor_id,
#                 'quantity': quantity
#             }
#             FreezerInventory.save(data)

#         flash(f'{quantity} {name} added to the freezer at {ice_cream_shop.name}!', 'success')
#         return redirect(url_for('ice_cream_shop', ice_cream_shop_id=ice_cream_shop.id))

#     return render_template('add_flavor_to_freezer.html', ice_cream_shops=ice_cream_shops)