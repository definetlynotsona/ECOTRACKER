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
@auth.route('/details', methods=['GET', 'POST'])
def submit():
    pickup_details = None
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        address = request.form.get('address')
        email = request.form.get('email')
        pick_up = request.form.get('pick_up')
        quantity = request.form.get('quantity')
        phone = request.form.get('phone')  # Corrected form field name
        date = request.form.get('date')
        time = request.form.get('time')

        # Create a new PickupDetails object
        new_pickup = Pickup_Details(name=name, address=address, email=email, pickup_point=pick_up,
                                   quantity=quantity, contact_no=phone, date=date, time_slot=time)
        # Add the new pickup to the database session and commit changes
        db.session.add(new_pickup)
        db.session.commit()
# Retrieve the newly added pickup details
         # Assuming name is unique
        pickup_details = Pickup_Details.query.filter_by(name=name).first()
        # Print pickup_details for debugging
        print("Pickup Details:", pickup_details)

        # Check if pickup_details is not None before generating PDF content
        if pickup_details:
            # Generate PDF receipt content with the pickup details
            pdf_content = generate_pdf_content(pickup_details)

            # Create response with PDF data
            response = make_response(pdf_content)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=receipt.pdf'
            return response
        else:
            return "Error: Pickup details not found."

        return redirect(url_for('views.home'))
    else:
        # Handle the GET request
        return render_template('details.html')

def generate_pdf_content(pickup_details):
    # Check if pickup_details is None
    if pickup_details is None:
        print("Error: Pickup details is None.")
        return "Error: Pickup details not found."

    try:
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=12)

        # Organize data into rows and columns
        data = [
            ("Name:", pickup_details.name),
            ("Address:", pickup_details.address),
            ("Email:", pickup_details.email),
            ("Pickup Point:", pickup_details.pickup_point),
            ("Quantity:", pickup_details.quantity),
            ("Contact No:", pickup_details.contact_no),
            ("Date:", pickup_details.date),
            ("Time Slot:", pickup_details.time_slot)
        ]

        # Add data to PDF in rows and columns
        col_width = 70
        row_height = 10
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height, txt=str(item), border=1)  # Ensure item is converted to string
            pdf.ln(row_height)  # Move to the next line for the next row

        # Generate PDF output
        pdf_output = pdf.output(dest='S').encode('latin1')

        return pdf_output

    except Exception as e:
        print("Error generating PDF content:", e)
        return "Error generating PDF content."

@auth.route('/donate', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        # Get form data
        trash_type = request.form.get('trashtype')
        trash_variety = request.form.get('trashvariety')
        trash_weight = float(request.form.get('trashweight'))
        total_price = request.form.get('total_price')
        

        # Create a new Donation object
        new_donation = Donation(type=trash_type, variety=trash_variety, weight=trash_weight, total_price=total_price)

        # Add the new donation to the database session and commit changes
        db.session.add(new_donation)
        db.session.commit()

        return redirect(url_for('views.donate'))
    else:
        # Handle the GET request
        return render_template('donate.html')
