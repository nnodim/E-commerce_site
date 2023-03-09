from flask import render_template, session, request, redirect, url_for, flash, current_app, make_response
# from flask_login import login_required, current_user, logout_user, login_user
from app import app, db, photos, search, bcrypt
from app.customers.form import CustomerRegisterForm
from app.customers.models import Register
import secrets
import os


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password,
                            country=form.country.data, city=form.city.data, contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Registration complete. Please Login', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)
