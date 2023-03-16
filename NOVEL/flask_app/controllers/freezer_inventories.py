from flask_app import app
from flask_login import current_user
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.freezer_inventory import FreezerInventory
from flask_app.models.flavor import Flavor

DATABASE = 'novel_app'



@app.route('/freezer_inventories')
def freezer_inventories():
    user = User.get_one_by_id(int(session['id']))
    freezer_inventories = FreezerInventory.get_all()
    return render_template('freezer_inventory.html', freezer_inventories=freezer_inventories)



@app.route('/freezer_inventories/<int:inventory_id>/edit', methods=['GET'])
def edit_freezer_inventory(inventory_id):
    freezer_inventory = FreezerInventory.get_one_by_id(inventory_id)
    return render_template('edit_freezer_inventory.html', freezer_inventory=freezer_inventory)


@app.route('/freezer_inventories/update/<int:inventory_id>', methods=['POST'])
def update_freezer_inventory(inventory_id):
    quantity = request.form['quantity']

    data = {
        'id': inventory_id,
        'quantity': quantity,
    }

    FreezerInventory.update(data)

    return redirect('/freezer_inventories')


@app.route('/freezer_inventories/<int:inventory_id>/delete', methods=['POST'])
def delete_freezer_inventory(inventory_id):
    FreezerInventory.delete(inventory_id)
    flash('Freezer inventory record deleted successfully!', 'success')

    return redirect('/freezer_inventories')