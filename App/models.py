from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_pokemons = db.relationship('UserPokemon', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id} {self.username} - {self.email}>'

    def catch_pokemon(self, pokemon_id, name):
        user_pokemon = UserPokemon(user_id=self.id, pokemon_id=pokemon_id, name=name)
        db.session.add(user_pokemon)
        db.session.commit()

    def release_pokemon(self, pokemon_id, name):
        user_pokemon = UserPokemon.query.filter_by(user_id=self.id, pokemon_id=pokemon_id, name=name).first()
        if user_pokemon:
            db.session.delete(user_pokemon)
            db.session.commit()

    def rename_pokemon(self, pokemon_id, name):
        user_pokemon = UserPokemon.query.filter_by(user_id=self.id, pokemon_id=pokemon_id).first()
        if user_pokemon:
            user_pokemon.name = name
            db.session.commit()

class UserPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, pokemon_id, name):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
        self.name = name

    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pokemon_id': self.pokemon_id,
            'name': self.name
        }

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    sp_attack = db.Column(db.Integer, nullable=False)
    sp_defense = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    type1 = db.Column(db.String(50), nullable=False)
    type2 = db.Column(db.String(50))

    def __init__(self, name, attack, defense, hp, height, sp_attack, sp_defense, speed, type1, type2=None):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.height = height
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.type1 = type1
        self.type2 = type2
        
    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'attack': self.attack,
            'defense': self.defense,
            'hp': self.hp,
            'height': self.height,
            'sp_attack': self.sp_attack,
            'sp_defense': self.sp_defense,
            'speed': self.speed,
            'type1': self.type1,
            'type2': self.type2
        }