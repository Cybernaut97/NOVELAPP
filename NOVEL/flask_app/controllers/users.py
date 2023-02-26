import re
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.ice_cream_shop import IceCreamShop
from flask_app.models.flavor import Flavor

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def landing():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.is_valid(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data ={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    session['id'] = User.newUser(data)

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash('Please login before trying to go to dashboard page')
        return redirect('/')
    user = User.get_one_by_id(int(session['id']))
    ice_cream_shops = IceCreamShop.get_all()
    ice_cream_flavors = []
    sorbet_flavors = []
    for shop in ice_cream_shops:
        current_flavors = shop.get_current_flavors()
        ice_cream_flavors += current_flavors['ice_cream_flavors']
        sorbet_flavors += current_flavors['sorbet_flavors']
    ice_cream_shop = ice_cream_shops[0]
    return render_template('dashboard.html', user=user, ice_cream_shops=ice_cream_shops, ice_cream_flavors=ice_cream_flavors, sorbet_flavors=sorbet_flavors, ice_cream_shop=ice_cream_shop)

@app.route('/login', methods=['POST'])
def login():
    user_to_check = User.get_one_by_email(request.form['email'])
    if not user_to_check: 
        flash('Invalid email/password combo')
        return redirect('/')
    if not bcrypt.check_password_hash(user_to_check.password, request.form['password']):
        flash('Invalid email/password combo')
        return redirect('/')
    session['id'] = user_to_check.id 
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash('user logged out')
    return redirect('/')



