import os, csv
from flask import Flask, jsonify, request
from functools import wraps
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from .models import db, User, UserPokemon, Pokemon

# Configure Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MySecretKey'
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config['JWT_HEADER_TYPE'] = ""
app.config['JWT_HEADER_NAME'] = "Cookie"


# Initialize App 
db.init_app(app)
app.app_context().push()
CORS(app)
jwt = JWTManager(app)

# Initializer Function to be used in both init command and /init route
def initialize_db():
  db.drop_all()
  db.create_all()

  with open('pokemon.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if 'height' key exists in the row
            if 'height' in row:
                height = int(row['height']) if row['height'] else None
                type2 = row['type2'] if row['type2'] else None
                pokemon = Pokemon(
                    name=row['name'],
                    attack=int(row['attack']),
                    defense=int(row['defense']),
                    hp=int(row['hp']),
                    height=height,
                    sp_attack=int(row['sp_attack']),
                    sp_defense=int(row['sp_defense']),
                    speed=int(row['speed']),
                    type1=row['type1'],
                    type2=type2
                )
                db.session.add(pokemon)
  db.session.commit()

# ********** Routes **************
@app.route('/')
def index():
  return '<h1>Poke API v1.0</h1>'

# GET List Pokemon route
@app.route('/list-pokemon', methods=['GET'])
def list_pokemon():
    initialize_db()
    return jsonify({"message": "List of Pokemon"})

# POST Sign Up - Success route
@app.route('/signup-success', methods=['POST'])
def signup_success():
    # Add your logic here for successful signup
    return jsonify({"message": "Sign Up successful"})

# POST Sign Up - Bad Username route
@app.route('/signup-bad-username', methods=['POST'])
def signup_bad_username():
    # Add your logic here for signup with a bad username
    return jsonify({"message": "Bad username"})

# POST Login - Bad ID route
@app.route('/login-bad-id', methods=['POST'])
def login_bad_id():
    # Add your logic here for login with a bad ID
    return jsonify({"message": "Bad ID"})

# POST Login - Success route
@app.route('/login-success', methods=['POST'])
def login_success():
    # Add your logic here for successful login
    return jsonify({"message": "Login successful"})

# POST Save My Pokemon route
@app.route('/save-my-pokemon', methods=['POST'])
def save_my_pokemon():
    # Add your logic here to save a Pokemon for a user
    return jsonify({"message": "Pokemon saved successfully"})

# POST Save My Pokemon Bad ID route
@app.route('/save-my-pokemon-bad-id', methods=['POST'])
def save_my_pokemon_bad_id():
    # Add your logic here for saving a Pokemon with a bad ID
    return jsonify({"message": "Bad ID"})

# GET List My Pokemon route
@app.route('/list-my-pokemon', methods=['GET'])
def list_my_pokemon():
    # Add your logic here to fetch and return a list of a user's Pokemon
    return jsonify({"message": "List of My Pokemon"})

# GET Get My Pokemon Success route
@app.route('/get-my-pokemon-success', methods=['GET'])
def get_my_pokemon_success():
    # Add your logic here for successfully getting a user's Pokemon
    return jsonify({"message": "Get My Pokemon successful"})

# GET Get My Pokemon - Bad ID route
@app.route('/get-my-pokemon-bad-id', methods=['GET'])
def get_my_pokemon_bad_id():
    # Add your logic here for getting a user's Pokemon with a bad ID
    return jsonify({"message": "Bad ID"})

# PUT Update My Pokemon route
@app.route('/update-my-pokemon', methods=['PUT'])
def update_my_pokemon():
    # Add your logic here to update a user's Pokemon
    return jsonify({"message": "Update My Pokemon successful"})

# PUT Update My Pokemon - Bad ID route
@app.route('/update-my-pokemon-bad-id', methods=['PUT'])
def update_my_pokemon_bad_id():
    # Add your logic here for updating a user's Pokemon with a bad ID
    return jsonify({"message": "Bad ID"})

# DELETE Delete My Pokemon route
@app.route('/delete-my-pokemon', methods=['DELETE'])
def delete_my_pokemon():
    # Add your logic here to delete a user's Pokemon
    return jsonify({"message": "Delete My Pokemon successful"})

# DELETE Delete My Pokemon - Bad ID route
@app.route('/delete-my-pokemon-bad-id', methods=['DELETE'])
def delete_my_pokemon_bad_id():
    # Add your logic here for deleting a user's Pokemon with a bad ID
    return jsonify({"message": "Bad ID"})

# Initialize Database Route
@app.route('/init', methods=['GET'])
def init():
    # Add your logic here to initialize the database
    # For example, you could call the initialize_db() function
    return jsonify({"message": "Database initialized"})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)

