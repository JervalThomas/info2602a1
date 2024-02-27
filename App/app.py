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

# POST Sign Up Route
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


# POST Login Route
@app.route('/login', methods=['POST'])
def login():
    login_data = request.json
    username = login_data.get('username')
    password = login_data.get('password')

    if username == 'example_user' and password == 'example_password':
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "bad username/password given"}), 401

# POST Save My Pokemon route
@app.route('/mypokemon', methods=['POST'])
def save_my_pokemon():
    pokemon_data = request.json
    username = pokemon_data.get('name')
    pokemon_id = pokemon_data.get('pokemon_id')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": username, "User not found " : ""}), 404

    pokemon = Pokemon.query.get(pokemon_id)
    if not pokemon:
        return jsonify({"error": f"{pokemon_id} is not a valid pokemon id"}), 400

    pokemon_name = pokemon.name

    user_pokemon = UserPokemon(user_id=user.id, pokemon_id=pokemon_id, name=pokemon_name)
    db.session.add(user_pokemon)
    db.session.commit()

    message = f"{pokemon_name} captured with id: {user_pokemon.id}"
    return jsonify({"message": message, "id": user_pokemon.id, "name": pokemon_name}), 201

# GET List My Pokemon route
@app.route('/mypokemon', methods=['GET'])
def list_my_pokemon():
    request_data = request.json
    username = request_data.get('name')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_pokemon = UserPokemon.query.filter_by(user_id=user.id).all()

    pokemon_list = []
    for user_poke in user_pokemon:
        pokemon = Pokemon.query.get(user_poke.pokemon_id)
        if not pokemon:
            continue

        pokemon_data = {
            "id": pokemon.id,
            "name": pokemon.name,
            "species": pokemon.type1
        }
        pokemon_list.append(pokemon_data)

    return jsonify(pokemon_list)

# GET Get My Pokemon Success route
@app.route('/mypokemon/<int:user_id>', methods=['GET'])
def get_my_pokemon(user_id):
    user_pokemon_list = UserPokemon.query.filter_by(user_id=user_id).all()
    if not user_pokemon_list:
        return jsonify({"error": f"Id {user_id} is invalid or does not belong to the user"}), 401

    pokemon_list = []
    for user_pokemon in user_pokemon_list:
        pokemon = Pokemon.query.get(user_pokemon.pokemon_id)
        if not pokemon:
            continue

        response_data = {
            "id": user_pokemon.id,
            "name": pokemon.name,
            "species": pokemon.type1
        }
        pokemon_list.append(response_data)

    return jsonify({"pokemon": pokemon_list})

# PUT Update My Pokemon route
@app.route('/mypokemon/1', methods=['PUT'])
def update_my_pokemon():
    # Add your logic here to update a user's Pokemon
    return jsonify({"message": "Update My Pokemon successful"})

# PUT Update My Pokemon - Bad ID route

# DELETE Delete My Pokemon route
@app.route('/mypokemon/1', methods=['DELETE'])
def delete_my_pokemon():
    # Add your logic here to delete a user's Pokemon
    return jsonify({"message": "Delete My Pokemon successful"})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)

