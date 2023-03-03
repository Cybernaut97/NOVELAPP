
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.models.flavor import Flavor



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
