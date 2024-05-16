from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

class Pickup_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Make the name field nullable
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pickup_point = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)  # Changed to string as per your previous change
    contact_no = db.Column(db.String(20), nullable=False)  # Adjust nullable based on your requirements
    date = db.Column(db.String(20), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    variety = db.Column(db.String(50))
    weight = db.Column(db.Float)
    total_price = db.Column(db.String(50))
