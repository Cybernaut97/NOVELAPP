from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.flavor import Flavor
from flask_app.models.ice_cream_shop import IceCreamShop
from twilio.rest import Client
from datetime import datetime, timedelta
from flask_app.models.freezer_inventory import FreezerInventory


# Define your Twilio account information here
account_sid = 'your_account_sid_here'
auth_token = 'your_auth_token_here'
client = Client(account_sid, auth_token)

# List of phone numbers to notify when a new flavor is added
customer_numbers = ['+15551234567', '+15557654321']

@app.route('/new')
def new_flavor():
    if 'id' not in session:
        flash('Please login')
        return redirect('/')
    user = User.get_one_by_id(int(session['id']))
    flavors = Flavor.get_all()
    flavor = None  
    return render_template('new_flavor.html', user=user, flavors=flavors, flavor=flavor)
    print(type(request.form['is_ice_cream']))

@app.route('/flavors')
def ice_cream_flavors():
    ice_cream_flavors = Flavor.get_all()
    sorbet_flavors = Flavor.get_all()
    shop_id = request.args.get('shop_id')
    if shop_id:
        shop = IceCreamShop.get_one_by_id({'id': shop_id})
        if not shop:
            flash(f"Ice cream shop with id {shop_id} does not exist")
            return redirect('/flavors')
    else:
        shop = None
    return render_template('flavors.html', ice_cream_flavors=ice_cream_flavors, sorbet_flavors=sorbet_flavors, shop=shop)

@app.route('/show/<int:flavor_id>')
def show(flavor_id):
    if 'id' not in session:
        flash('Please login before trying to go to dashboard page')
        return redirect('/')
    user = User.get_one_by_id(int(session['id']))
    flavor = Flavor.get_one_by_id(flavor_id)
    return render_template('show.html', user=user, flavor=flavor)


@app.route('/create', methods=['POST'])
def create_flavor():
    if 'id' not in session:
        flash('Please login')
        return redirect('/')
    if not Flavor.is_valid(request.form):
        return redirect('/new')

    # this is to check if flavor is a Ice cream or Sorbet flavors
    is_ice_cream = request.form['is_ice_cream'].lower() == 'true'

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'is_ice_cream': is_ice_cream
    }
    Flavor.save(data)
    return redirect('/flavors')


@app.route('/show/<int:flavor_id>')
def view(flavor_id):
    if 'id' not in session:
        flash('Please login before trying access restricted pages')
        return redirect('/')
    flavor = Flavor.get_one_by_id(flavor_id)
    user = User.get_one_by_id(session['id'])
    return render_template('show.html', flavor=flavor, user=user)


@app.route('/edit/<int:flavor_id>/edit')
def edit(flavor_id):
    if 'id' not in session:
        flash('Please login')
        return redirect('/')
    flavor = Flavor.get_one_by_id(flavor_id)
    user = User.get_one_by_id(session['id'])
    return render_template('edit_flavor.html', flavor=flavor, user=user)


@app.route("/update/<int:flavor_id>/update", methods=["POST"])
def update(flavor_id):
    if 'id' not in session:
        flash('Please login')
    if not Flavor.is_valid(request.form):
        return redirect(f'/edit/{flavor_id}/edit')

    is_ice_cream = True if request.form.get('is_ice_cream') == '1' else False

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'is_ice_cream': is_ice_cream,
        'id': flavor_id
    }
    
    query = "UPDATE flavors SET name = %(name)s, is_ice_cream = %(is_ice_cream)s, description = %(description)s WHERE id = %(id)s;"
    Flavor.edit(query, data, flavor_id)
    
    user = User.get_one_by_id(session['id'])
    return redirect('/flavors')

@app.route("/delete/<int:flavor_id>/delete", methods=["POST"])
def delete(flavor_id):
    if 'id' not in session:
        return redirect('/')
    Flavor.delete(flavor_id)
    return redirect('/flavors')

# @app.route('/add_to_freezer/<int:flavor_id>/<int:shop_id>', methods=['GET', 'POST'])
# def add_to_freezer(flavor_id, shop_id):
#     flavor = Flavor.get_one_by_id(flavor_id)
#     ice_cream_shop = IceCreamShop.get_one_by_id(shop_id)
#     ice_cream_shops = IceCreamShop.get_all()
#     if request.method == 'POST':
#         data = {
#             'shop_id': request.form['ice_cream_shop_id'],
#             'flavor_id': flavor_id,
#             'quantity': request.form['quantity']
#         }
#         FreezerInventory.save(data)
#         flash(f"{flavor.name} added to {ice_cream_shop.name}'s freezer inventory!")
#         return redirect(f'/ice_cream_shops/{shop_id}')
#     return render_template('add_to_freezer.html', flavor=flavor, ice_cream_shop=ice_cream_shop, ice_cream_shops=ice_cream_shops)

@app.route('/remove_flavor', methods=['POST'])
def remove_flavor():
    # Get the ID of the flavor to remove
    flavor_id = int(request.form['flavor_id'])

    # Remove the flavor from the current list
    ice_cream_shop = IceCreamShop.get_one_by_id(1) # Replace 1 with the actual ID of the ice cream shop
    ice_cream_shop.remove_current_flavor(flavor_id)

    # Redirect back to the current flavors page
    return redirect('/current_flavors')

@app.route('/ice_cream_shop/flavors/<int:ice_cream_shop_id>', methods=['POST'])
def set_flavor(ice_cream_shop_id):
    if 'id' not in session:
        return redirect('/login')

    flavor_id = request.form.get('flavor_id')
    if not flavor_id:
        flash('Please select a flavor')
        return redirect(f'/ice_cream_shop/flavors/{ice_cream_shop_id}')

    # Check if the flavor is being added to the current list
    ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
    if flavor_id in ice_cream_shop.current_flavors:
        # Get the name of the flavor
        flavor = Flavor.get_one_by_id(flavor_id)
        flavor_name = flavor.name

        # Schedule the SMS notification to be sent 5 minutes later
        scheduled_time = datetime.now() + timedelta(minutes=5)
        for number in customer_numbers:
            message = client.messages.create(
                to=number,
                from_='+1415XXXXXXX', # Replace with your Twilio phone number
                body = f'New flavor alert! {flavor_name} is now available at Novel Ice Cream Shop. Hurry in to try it!',
                scheduled_time=scheduled_time
            )

    # Add the flavor to the ice cream shop
    IceCreamShop.add_flavor(ice_cream_shop_id, flavor_id)
    return redirect(f'/ice_cream_shop/{ice_cream_shop_id}')