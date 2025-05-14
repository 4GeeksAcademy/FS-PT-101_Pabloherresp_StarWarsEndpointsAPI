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
from models import db, Users, Pokemons, Cities, Regions, Favs
from sqlalchemy import select

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

@app.route('/users', methods=['GET'])
def get_users():
    stmt = select(Users)
    users = db.session.execute(stmt).scalars().all()
    response_body = [user.serialize() for user in users]
    return jsonify(response_body), 200

@app.route('/pokemons', methods=['GET'])
def get_pokemons():
    stmt = select(Pokemons)
    pokemons = db.session.execute(stmt).scalars().all()
    response_body = [pokemon.serialize() for pokemon in pokemons]
    return jsonify(response_body), 200

@app.route('/cities', methods=['GET'])
def get_cities():
    stmt = select(Cities)
    cities = db.session.execute(stmt).scalars().all()
    response_body = [city.serialize() for city in cities]
    return jsonify(response_body), 200

@app.route('/regions', methods=['GET'])
def get_regions():
    stmt = select(Regions)
    regions = db.session.execute(stmt).scalars().all()
    response_body = [region.serialize() for region in regions]
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
