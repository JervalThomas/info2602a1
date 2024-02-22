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
from werkzeug.exceptions import HTTPException

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

    with open('pokemon.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            abilities = row['abilities']
            attack = int(row['attack'])
            defense = int(row['defense'])
            hp = int(row['hp'])
            height = float(row['height_m']) if row['height_m'] else None
            sp_attack = int(row['sp_attack'])
            sp_defense = int(row['sp_defense'])
            speed = int(row['speed'])
            type1 = row['type1']
            type2 = row['type2'] if row['type2'] else None
            name = row['name']
            weight = float(row['weight_kg']) if row['weight_kg'] else None

            pokemon = Pokemon(
                name=name,
                attack=attack,
                defense=defense,
                hp=hp,
                height=height,
                weight=weight,
                sp_attack=sp_attack,
                sp_defense=sp_defense,
                speed=speed,
                type1=type1,
                type2=type2
            )
            db.session.add(pokemon)

    db.session.commit()


# ********** Routes **************
@app.route('/')
def index():
  return '<h1>Poke API v1.0</h1>'

# Initialize Database Route
@app.route('/init', methods=['GET'])
def init():
    initialize_db()
    return jsonify({"message": "Database Initialized!"})

# GET List Pokemon route
@app.route('/pokemon', methods=['GET'])
def list_pokemon():
    all_pokemon = Pokemon.query.all()
    
    pokemon_list = []
    for pokemon in all_pokemon:
        pokemon_data = pokemon.get_json()
        pokemon_list.append(pokemon_data)
    return jsonify({"pokemon": pokemon_list})

# POST Sign Up - Success route
@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    username = user_data.get('username')
    email = user_data.get('email')

    existing_username = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()
    
    if existing_username or existing_email:
        return jsonify({"message": "Username or email already exists"}), 400

    user = User(username=username, email=email, password=user_data.get('password'))
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": f"{username} created"}), 201


# POST Login - Bad ID route
@app.route('/login', methods=['POST'])
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

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)

