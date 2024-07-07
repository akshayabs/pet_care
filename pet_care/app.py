from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['mydb']
users_collection = db['login']  # Collection for user data
booking_collection = db['bookings']  # Collection for bookings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        # Check if the email already exists
        if users_collection.find_one({'email': email}):
            return render_template('login.html', error='Email already exists. Please choose another email.')
        
        users_collection.insert_one({'email': email, 'password': hashed_password})
        return redirect(url_for('book'))

    return render_template('login.html')

    

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        pet_name = request.form.get('pet_name')
        dob=request.form.get('boarding_date')
        phone=request.form.get('phone')
        message=request.form.get('message')
        booking_data = {
            'name': name,
            'email': email,
            'pet_name': pet_name,
            'boarding_date': dob,
            'phone': phone,
            'message': message
        }

        booking_collection.insert_one(booking_data)

        return redirect(url_for('index'))

    return render_template('book.html')


if __name__ == '__main__':
    app.run(debug=True)
