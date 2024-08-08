"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import db, People, Species, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET', 'POST'])
def handle_people():
    if request.method == "POST":
        name = request.json["name"]
        description = request.json["description"]
        new_person = People(
            name = name,
            description = description
        )
        return jsonify(new_person.serialize()), 201
    people = People.query.all()
    people_dictionaries = []
    for person in people:
        people_dictionaries.append(
            person.serialize()
        )
    return jsonify(people_dictionaries), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({
            "msg": 'Character not found'
        }), 404
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    if request.method == "POST":
        name = request.json["name"]
        population = request.json["population"]
        description = request.json["description"]
        new_planet = Planets(
            name = name,
            population = population,
            description = description
        )
        return jsonify(new_planet.serialize()), 201
    planets = Planets.query.all()
    planets_dictionaries = []
    for planet in planets:
        planets_dictionaries.append(
            planet.serialize()
        )
    return jsonify(planets_dictionaries), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({
            "msg": 'Planet not found'
        }), 404
    return jsonify(planet.serialize()), 200

@app.route('/species', methods=['GET', 'POST'])
def handle_species():
    if request.method == "POST":
        name = request.json["name"]
        language = request.json["language"]
        description = request.json["description"]
        new_specie = Planets(
            name = name,
            language = language,
            description = description
        )
        return jsonify(new_specie.serialize()), 201
    species = Species.query.all()
    species_dictionaries = []
    for specie in species:
        species_dictionaries.append(
            specie.serialize()
        )
    return jsonify(species_dictionaries), 200

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == "POST":
        email = request.json.get('email')
        username = request.json.get('username')
        if not email or not username:
            return jsonify({
                "msg": 'Email and username are required'
            }), 400
        new_user = User(
            email = email, 
            username = username
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({
            "msg": 'User not found'
        }), 404
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/favorites/planets/<int:planets_uid>', methods=['POST'])
def add_favorite_planet(planets_uid):
    user_id = request.json.get('user_id')
    favorite = Favorites(user_id=user_id, planets_uid=planets_uid)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
