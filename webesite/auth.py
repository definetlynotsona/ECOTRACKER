from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from  werkzeug.security import generate_password_hash, check_password_hash
from . import  db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid username or password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email =request.form.get('email')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        contact_num = request.form.get('contactnum')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='errror')
        elif len(email) > 30:
            flash('Incorrect email', category='error')
        elif len(first_name) < 2:
            flash('No name', category='error')
        elif len(last_name) < 2:
            flash('Invalid Last Name', category='error')
        elif len(password1) < 7:
            flash('Incorrect password', category='error')
        elif password1 != password2:
            flash('Password must be over 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name,password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)