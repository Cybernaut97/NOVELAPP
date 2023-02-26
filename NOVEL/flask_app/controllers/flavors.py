from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.flavor import Flavor
from flask_app.models.ice_cream_shop import IceCreamShop


@app.route('/new')
def new_flavor():
    if 'id' not in session:
        flash('Please login')
        return redirect('/')
    user = User.get_one_by_id(int(session['id']))
    flavors = Flavor.get_all()
    flavor = None  # add this line to define an empty flavor object
    return render_template('new_flavor.html', user=user, flavors=flavors, flavor=flavor)
    print(type(request.form['is_ice_cream']))


@app.route('/flavors')
def flavors():
    all_flavors = Flavor.get_all()
    return render_template('flavors.html', flavors=all_flavors)

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

    # Convert is_ice_cream value to a boolean
    is_ice_cream = request.form['is_ice_cream'].lower() == 'true'

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'is_ice_cream': is_ice_cream
    }
    Flavor.save(data)
    return redirect('/dashboard')


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


@app.route("/update/<int:flavor_id>/update", methods =["POST"])
def update(flavor_id):
    if 'id' not in session:
        flash('Please login')
    if not Flavor.is_valid(request.form):
        return redirect(f'/edit/{flavor_id}/edit')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'id': flavor_id
        }
    Flavor.edit(data)
    user = User.get_one_by_id(session['id'])
    return redirect('/flavors')

@app.route("/delete/<int:flavor_id>/delete", methods=["POST"])
def delete(flavor_id):
    if 'id' not in session:
        return redirect('/')
    Flavor.delete(flavor_id)
    return redirect('/flavors')

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

    IceCreamShop.add_flavor(ice_cream_shop_id, flavor_id)
    return redirect(f'/ice_cream_shop/{ice_cream_shop_id}')