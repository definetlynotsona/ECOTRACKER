from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email =request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(email) > 30:
            flash('Incorrect email', category='error')
        elif len(firstname) < 2:
            flash('No name', category='error')
        elif len(lastname) < 2:
            flash('Invalid Last Name', category='error')
        elif len(password1) < 7:
            flash('Incorrect password', category='error')
        elif password1 != password2:
            flash('Password must be over 7 characters', category='error')
        else:
            flash('Account Created!', category='success')
            
    return render_template('signup.html')