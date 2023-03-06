
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

DATABASE = 'novel_app'


@app.route('/ice_cream_shops', methods=['GET', 'POST'])
def ice_cream_shops():
    if request.method == 'POST':
        user_id = request.form['user_id']
        shop_id = request.form['shop_id']
        assign_user_to_shop(int(user_id), int(shop_id))
    ice_cream_shops = IceCreamShop.get_all()
    users = User.get_all()
    return render_template('ice_cream_shops.html', ice_cream_shops=ice_cream_shops, users=users)


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

@app.route('/assign_user_to_shop/<int:shop_id>', methods=['POST'])
def assign_user_to_shop(shop_id):
    print(request.args)
    user_id = request.args.get('user_id')
    if user_id is None:
        flash('User ID not found in URL parameters', 'error')
        return redirect('/ice_cream_shops')

    user_id = request.form['user_id']
    ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
    user = User.get_one_by_id(user_id)
    user.shop_id = shop_id
    user.update()
    flash('User assigned to shop!', 'success')
    return redirect('/ice_cream_shops')