from flask import Blueprint, render_template
from flask_login import  login_required,  current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@views.route('/about')
@login_required
def about():
    return render_template('about.html', user=current_user)

@views.route('/learn')
@login_required
def learn():
    return render_template('learn.html', user=current_user)

@views.route('/details')
@login_required
def details():
    return render_template('details.html', user=current_user)

@views.route('/donate')
@login_required
def donate():
    return render_template('donate.html', user=current_user)
