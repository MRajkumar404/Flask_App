from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.cli.command('create-db')
def create_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created.")


# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loginform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db = SQLAlchemy(app)

@app.route('/',methods=['GET'])

def index():
    
    # Pass the data to the HTML template
    return render_template('index.html')

@app.route('/',methods=['POST'])
def add():
    data = request.form['usr_na']
    print(data)
    return redirect('/')


if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
