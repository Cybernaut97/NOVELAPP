from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash, url_for
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
    # print(type(request.form['is_ice_cream']))


@app.route('/flavors')
def flavors():
    user = User.get_one_by_id(session['id'])
    ice_cream_flavors = Flavor.get_ice_cream_flavors()
    sorbet_flavors = Flavor.get_sorbet_flavors()
    ice_cream_shop_id = request.args.get('ice_cream_shop_id')
    ice_cream_shop = None 

    if ice_cream_shop_id:
        ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
        if not ice_cream_shop:
            flash(f"Ice cream shop with id {ice_cream_shop_id} does not exist")
            return redirect('/flavors')

    print(f"Ice Cream Shop: {ice_cream_shop}")
    print(f"Session ID: {session.get('id')}")
    if ice_cream_shop:
        print(f"Ice Cream Shop User ID: {ice_cream_shop.user_id}")
    return render_template('flavors.html', ice_cream_flavors=ice_cream_flavors, sorbet_flavors=sorbet_flavors, ice_cream_shop=ice_cream_shop, user_id=user.id)


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
    user = User.get_one_by_id(session['id'])
    return redirect('/ice_cream_shops')


@app.route('/show/<int:flavor_id>')
def view(flavor_id):
    if 'id' not in session:
        flash('Please login before trying access restricted pages')
        return redirect('/')
    flavor = Flavor.get_one_by_id(flavor_id)
    user = User.get_one_by_id(session['id'])
    return render_template('show.html', flavor=flavor, user=user )


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
def delete_flavor(flavor_id):
    if 'id' not in session:
        return redirect('/')
    Flavor.delete(flavor_id)
    return redirect(url_for('flavors'))

@app.route('/remove_flavor', methods=['POST'])
def remove_flavor():
    # Get the ID of the flavor to remove
    flavor_id = int(request.form['flavor_id'])

    # Remove the flavor from the current list
    ice_cream_shop = IceCreamShop.get_one_by_id(1) # Replace 1 with the actual ID of the ice cream shop
    ice_cream_shop.remove_current_flavor(flavor_id)

    # Redirect back to the current flavors page
    return redirect('/current_flavors')


