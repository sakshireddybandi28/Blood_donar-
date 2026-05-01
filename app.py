from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "blood_donation_secret_key"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["blood_donation_db"]
contacts_collection = db["contacts"]
emergency_collection = db["emergencies"]
donors_collection = db["donors"]
users_collection = db["users"]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/offline')
def offline():
    return render_template('offline.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if users_collection.find_one({"email": email}):
            flash("Email already registered!", "danger")
            return redirect(url_for('signup'))
            
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        flash("Account created! Please login.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users_collection.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    blood_groups = [
        {"name": "A+ Positive", "price": 85, "stock": 75},
        {"name": "A- Negative", "price": 95, "stock": 30},
        {"name": "B+ Positive", "price": 80, "stock": 90},
        {"name": "B- Negative", "price": 99, "stock": 20},
        {"name": "O+ Positive", "price": 75, "stock": 85},
        {"name": "O- Negative", "price": 90, "stock": 15},
        {"name": "AB+ Positive", "price": 92, "stock": 45},
        {"name": "AB- Negative", "price": 98, "stock": 10},
    ]
    return render_template('services.html', blood_groups=blood_groups)

@app.route('/emergency', methods=['POST'])
def emergency():
    patient_name = request.form.get('patient_name')
    blood_group = request.form.get('blood_group')
    hospital = request.form.get('hospital')
    phone = request.form.get('phone')
    
    if patient_name and blood_group and hospital and phone:
        emergency_collection.insert_one({
            "patient_name": patient_name,
            "blood_group": blood_group,
            "hospital": hospital,
            "phone": phone,
            "status": "Pending"
        })
        flash("Emergency request sent! We are notifying nearby donors.", "success")
    else:
        flash("Please fill all emergency details.", "danger")
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            contacts_collection.insert_one({
                "name": name,
                "email": email,
                "message": message
            })
            flash("Message sent successfully!", "success")
            return redirect(url_for('contact'))
        else:
            flash("Please fill in all fields.", "danger")
            
    return render_template('contact.html')

@app.route('/register_donor', methods=['POST'])
def register_donor():
    name = request.form.get('name')
    blood_group = request.form.get('blood_group')
    location = request.form.get('location')
    phone = request.form.get('phone')
    
    if name and blood_group and location and phone:
        donors_collection.insert_one({
            "name": name,
            "blood_group": blood_group,
            "location": location,
            "phone": phone
        })
        flash("Thank you for registering as a donor! You are now a life-saver.", "success")
    else:
        flash("Please fill all registration details.", "danger")
    return redirect(url_for('services'))

if __name__ == '__main__':
    app.run(debug=True)
