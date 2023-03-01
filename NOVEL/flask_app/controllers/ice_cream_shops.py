
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.models.flavor import Flavor
from flask_app.models.freezer_inventory import FreezerInventory


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
    IceCreamShop.delete(ice_cream_shop_id)
    return redirect('/ice_cream_shops')

@app.route('/add_to_freezer/<int:flavor_id>', methods=['GET', 'POST'])
def add_to_freezer(flavor_id):
    if 'id' not in session:
        flash('Please login before trying to add to freezer')
        return redirect('/')
    
    ice_cream_shops = IceCreamShop.get_all()
    
    if request.method == 'POST':
        # Get the ice cream shop and the flavor
        shop_id = request.form.get('shop_id')
        quantity = request.form.get('quantity')
        print(f'shop_id: {shop_id}, quantity: {quantity}')
        flavor = Flavor.get_one_by_id(flavor_id)
        if flavor is None:
            flash('Flavor not found')
            return redirect('/')
        if shop_id is None or quantity is None:
            flash('Please select an ice cream shop and enter a quantity')
            return redirect(f'/add_to_freezer/{flavor_id}')
        shop = IceCreamShop.get_one_by_id(int(shop_id))
        if shop is None:
            flash('Ice cream shop not found')
            return redirect('/')
        # Add the flavor to the shop's freezer inventory
        freezer = FreezerInventory.get_one_by_shop_id_and_flavor_id(int(shop_id), flavor_id)
        if freezer is not None:
            # If the flavor is already in the freezer, just increment the quantity
            freezer.quantity += int(quantity)
            freezer.save()
        else:
            # Otherwise, add a new freezer inventory record for the flavor
            freezer = FreezerInventory(shop_id=int(shop_id), flavor_id=flavor_id, quantity=int(quantity))
            freezer.save()
        flash(f'{quantity} pans of {flavor.name} added to freezer inventory for ice cream shop {shop.name}')
        return redirect(f'/add_to_freezer/{flavor_id}?shop_id={shop_id}')
    else:
        # Get the ice cream shop and the flavor
        shop_id = request.args.get('shop_id')
        flavor = Flavor.get_one_by_id(flavor_id)
        if flavor is None:
            flash('Flavor not found')
            return redirect('/')
        return render_template('add_to_freezer.html', flavor=flavor, ice_cream_shops=ice_cream_shops, shop_id=shop_id)