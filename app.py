from flask import Flask, flash, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loginform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users, show_signup=True)

@app.route('/add', methods=['POST'])
def add():
    user_name = request.form['usr_na']
    email = request.form['usr_em']
    password = request.form['usr_pas']
    confirm_password = request.form['usr_cnfr']

    # Regular expression for password validation
    password_regex = re.compile(r'^(?=.*\d)(?=.*[!@#$%^&*])[0-9a-zA-Z!@#$%^&*]{6,}$')

    if not password_regex.match(password):
        flash('Password must be at least 6 characters long and include at least one number and one special character.', 'error')
        users = User.query.all()
        return render_template('index.html', user_name=user_name, email=email, users=users, show_signup=True)

    if password != confirm_password:
        flash('Passwords do not match. Please try again.', 'error')
        users = User.query.all()
        return render_template('index.html', user_name=user_name, email=email, users=users, show_signup=True)

    new_user = User(username=user_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    flash('User added successfully!', 'success')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return redirect('https://www.google.com')  # Redirect to another website
    else:
        flash('Invalid username or password.', 'error')
        return redirect('/')

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
