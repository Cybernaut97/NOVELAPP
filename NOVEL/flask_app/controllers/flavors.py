from flask_app import app
from flask_app import AUTHORIZED_USER_IDS
from flask_caching import Cache
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.flavor import Flavor
from flask_app.models.ice_cream_shop import IceCreamShop
from twilio.rest import Client
from datetime import datetime, timedelta
from flask_app.models.freezer_inventory import FreezerInventory
from flask import jsonify 


# cache for flavors 
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

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
    ice_cream_shop_id = request.args.get('ice_cream_shop_id')
    if session['id'] not in AUTHORIZED_USER_IDS:
        flash('You do not have permission to create flavors! Get Permission from Frank.. ')
        return redirect('/dashboard')
    
    user = User.get_one_by_id(int(session['id']))
    flavors = Flavor.get_all(ice_cream_shop_id)
    flavor = None  
    return render_template('new_flavor.html', user=user, flavors=flavors, flavor=flavor)
    # print(type(request.form['is_ice_cream']))


@app.route('/flavors')
@cache.cached(timeout=10)
def flavors():
    user = User.get_one_by_id(session['id'])
    ice_cream_flavors = Flavor.get_ice_cream_flavors()
    sorbet_flavors = Flavor.get_sorbet_flavors()
    ice_cream_shop_id = request.args.get('ice_cream_shop_id', None)
    ice_cream_shop = None 

    if ice_cream_shop_id:
        try:
            ice_cream_shop = IceCreamShop.get_one_by_id(ice_cream_shop_id)
        except Exception as e:
            flash(str(e))
            return redirect('/dashboard')

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
        return redirect('/dashboard')

    # this is to check if flavor is a Ice cream or Sorbet flavors
    is_ice_cream = request.form['is_ice_cream'].lower() == 'true'

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'is_ice_cream': is_ice_cream
    }
    Flavor.save(data)
    flash("flavor was added to master list ")
    user = User.get_one_by_id(session['id'])
    return redirect('/dashboard')


@app.route('/show/<int:flavor_id>')
def view(flavor_id):
    if 'id' not in session:
        flash('Please login before trying access restricted pages')
        return redirect('/')
    flavor = Flavor.get_one_by_id(flavor_id)
    user = User.get_one_by_id(session['id'])
    return render_template('show.html', flavor=flavor, user=user )


@app.route('/edit_flavor', methods=['GET', 'POST'])
def edit_flavor():
    if 'id' not in session:
        flash('Please login')
        return redirect('/')

    if session['id'] not in AUTHORIZED_USER_IDS:
        flash('You do not have permission to edit flavors.')
        return redirect('/dashboard')

    ice_cream_shop_id = request.args.get('ice_cream_shop_id')

    if request.method == 'POST':
        ice_cream_shop_id = request.form.get('ice_cream_shop_id')
        is_ice_cream = request.form.get('is_ice_cream') == 'True'

        data = {
            'id': request.form['flavor'],
            'name': request.form['name'],
            'description': request.form['description'],
            'is_ice_cream': is_ice_cream
        }
        Flavor.update(data)

        flash('Flavor updated successfully')
        return redirect('/dashboard')

    # Add the missing line to fetch the list of flavors
    flavors = Flavor.get_all(ice_cream_shop_id)  # Replace with your own method to fetch the list of flavors

    flavors_dicts = [flavor.to_dict() for flavor in flavors]
    return render_template('edit_flavor.html', flavors=flavors_dicts, ice_cream_shop_id=ice_cream_shop_id)


# @app.route('/edit/<int:flavor_id>/edit')
# def edit(flavor_id):
#     if 'id' not in session:
#         flash('Please login')
#         return redirect('/')
#     flavor = Flavor.get_one_by_id(flavor_id)
#     user = User.get_one_by_id(session['id'])
#     return render_template('edit_flavor.html', flavor=flavor, user=user) old edit 


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

@app.route("/delete_flavor", methods=["POST"])
def delete_flavor():
    flavor_id = request.form.get('flavor_id')
    ice_cream_shop_id = request.form.get('ice_cream_shop_id')

    print(f"flavor_id: {flavor_id}")
    print(f"ice_cream_shop_id: {ice_cream_shop_id}")

    if 'id' not in session:
        return redirect('/')

    # Get the flavor object before deleting it
    flavor_to_delete = Flavor.get_one_by_id(flavor_id)
    
    # Delete the flavor from the FreezerInventory and Flavor tables
    FreezerInventory.delete_by_flavor_id(flavor_id)
    Flavor.delete(flavor_id)

    # # Flash the message with the flavor name
    # if flavor_to_delete:
    #     flash(f'{flavor_to_delete.name} has been deleted from the database.', 'success')
    # else:
    #     flash('Flavor not found in the database.', 'error')
    
    return redirect(url_for('flavors', ice_cream_shop_id=ice_cream_shop_id))



@app.route('/remove_flavor', methods=['POST'])
def remove_flavor():
    # Get the ID of the flavor to remove
    flavor_id = int(request.form['flavor_id'])

    # Remove the flavor from the current list
    ice_cream_shop = IceCreamShop.get_one_by_id(1) # Replace 1 with the actual ID of the ice cream shop
    ice_cream_shop.remove_current_flavor(flavor_id)

    # Redirect back to the current flavors page
    return redirect('/current_flavors')


