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
from models import db, Users, Pokemons, Cities, Regions, Favs, Type
from sqlalchemy import select, delete

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

# USERS ENDPOINTS
@app.route('/users', methods=['GET'])
def get_users():
    stmt = select(Users)
    users = db.session.execute(stmt).scalars().all()
    response_body = [user.serialize() for user in users]
    return jsonify(response_body), 200

@app.route("/users/<int:user_id>", methods=['GET'])
def get_one_user(user_id):
    stmt = select(Users).where(Users.id == user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/users", methods=['POST'])
def create_user():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing fields for creating user."}), 400
    user = Users(email=data["email"], password=data["password"])
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't create user"}), 400
        
    return jsonify(user.serialize()), 200

@app.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    stmt = select(Users).where(Users.id == user_id)
    user = db.session.execute(stmt).scalar_one_or_none()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # eliminamos las entradas que referencian al usuario en la tabla favoritos
    stmt2 = delete(Favs).where(Favs.user_id == user_id)
    db.session.execute(stmt2)

    db.session.delete(user)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't delete user"}), 400
    return jsonify({"message": "User deleted"}), 200

@app.route("/users/<int:user_id>", methods=['PUT'])
def edit_user(user_id):
    pass

# POKEMONS ENDPOINTS
@app.route('/pokemons', methods=['GET'])
def get_pokemons():
    stmt = select(Pokemons)
    pokemons = db.session.execute(stmt).scalars().all()
    response_body = [pokemon.serialize() for pokemon in pokemons]
    return jsonify(response_body), 200

@app.route("/pokemons/<int:pokemon_id>", methods=['GET'])
def get_one_pokemon(pokemon_id):
    stmt = select(Pokemons).where(Pokemons.id == pokemon_id)
    pokemon = db.session.execute(stmt).scalar_one_or_none()
    if not pokemon:
        return jsonify({"error": "Pokemon not found"}), 404
    return jsonify(pokemon.serialize()), 200

@app.route("/pokemons", methods=['POST'])
def create_pokemon():
    data = request.json
    if not data or "name" not in data or "type1" not in data or "desc" not in data:
        return jsonify({"error": "Missing fields for creating pokemon."}), 400
    pokemon = Pokemons(name=data["name"], desc=data["desc"], type1=Type(data["type1"]), type2=Type(data["type2"]) if "type2" in data else None)
    db.session.add(pokemon)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't create pokemon"}), 400
        
    return jsonify(pokemon.serialize()), 200

@app.route("/pokemons/<int:pokemon_id>", methods=['DELETE'])
def delete_pokemon(pokemon_id):
    stmt = select(Pokemons).where(Pokemons.id == pokemon_id)
    pokemon = db.session.execute(stmt).scalar_one_or_none()

    if not pokemon:
        return jsonify({"error": "Pokemon not found"}), 404

    # eliminamos las entradas que referencian al pokemon en la tabla favoritos
    stmt2 = delete(Favs).where(Favs.pokemon_id == pokemon_id)
    db.session.execute(stmt2)

    db.session.delete(pokemon)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't delete Pokemon"}), 400
    return jsonify({"message": "Pokemon deleted"}), 200

# CITIES ENDPOINTS
@app.route('/cities', methods=['GET'])
def get_cities():
    stmt = select(Cities)
    cities = db.session.execute(stmt).scalars().all()
    response_body = [city.serialize() for city in cities]
    return jsonify(response_body), 200

@app.route("/cities/<int:city_id>", methods=['GET'])
def get_one_city(city_id):
    stmt = select(Cities).where(Cities.id == city_id)
    city = db.session.execute(stmt).scalar_one_or_none()
    if not city:
        return jsonify({"error": "City not found"}), 404
    return jsonify(city.serialize()), 200

@app.route("/cities", methods=['POST'])
def create_city():
    data = request.json
    if not data or "name" not in data or "population" not in data or "region_id" not in data:
        return jsonify({"error": "Missing fields for creating city."}), 400
    city = Cities(name=data["name"], population=data["population"], region_id=data["region_id"])
    db.session.add(city)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't create City"}), 400
        
    return jsonify(city.serialize()), 200

@app.route("/cities/<int:city_id>", methods=['DELETE'])
def delete_city(city_id):
    stmt = select(Cities).where(Cities.id == city_id)
    city = db.session.execute(stmt).scalar_one_or_none()

    if not city:
        return jsonify({"error": "City not found"}), 404

    # eliminamos las entradas que referencian a la ciudad en la tabla favoritos
    stmt2 = delete(Favs).where(Favs.city_id == city_id)
    db.session.execute(stmt2)

    db.session.delete(city)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't delete City"}), 400
    return jsonify({"message": "City deleted"}), 200

# REGIONS ENDPOINTS
@app.route('/regions', methods=['GET'])
def get_regions():
    stmt = select(Regions)
    regions = db.session.execute(stmt).scalars().all()
    response_body = [region.serialize() for region in regions]
    return jsonify(response_body), 200

@app.route("/regions/<int:region_id>", methods=['GET'])
def get_one_region(region_id):
    stmt = select(Regions).where(Regions.id == region_id)
    region = db.session.execute(stmt).scalar_one_or_none()
    if not region:
        return jsonify({"error": "Region not found"}), 404
    return jsonify(region.serialize()), 200

@app.route("/regions", methods=['POST'])
def create_region():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Missing fields for creating region."}), 400
    region = Regions(name=data["name"])
    db.session.add(region)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't create Region"}), 400
        
    return jsonify(region.serialize()), 200

@app.route("/regions/<int:region_id>", methods=['DELETE'])
def delete_region(region_id):
    stmt = select(Regions).where(Regions.id == region_id)
    region = db.session.execute(stmt).scalar_one_or_none()

    if not region:
        return jsonify({"error": "Region not found"}), 404

    # eliminamos las entradas que referencian a la región en la tabla favoritos
    stmt2 = delete(Favs).where(Favs.region_id == region_id)
    db.session.execute(stmt2)

    db.session.delete(region)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't delete Region, there might be some Cities attached to it"}), 400
    return jsonify({"message": "Region deleted"}), 200

# FAVS ENDPOINTS
@app.route("/favs", methods=["POST"])
def create_fav():
    data = request.json
    if not data or not "user_id" in data or not ("pokemon_id" in data or "city_id" in data or "region_id" in data):
        print("Vaya")
        return jsonify({"error": "Missing fields for creating fav."}), 400
    fav = Favs(
        user_id=data["user_id"],
        pokemon_id=data["pokemon_id"] if "pokemon_id" in data else 0,
        city_id=data["city_id"] if "city_id" in data else 0,
        region_id=data["region_id"] if "region_id" in data else 0
    )
    db.session.add(fav)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Couldn't create Fav"}), 400
        
    return jsonify({"message":"Fav created"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
