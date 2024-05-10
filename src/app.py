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
from models import db, User,People,Planets,Favoritos,Personaje_Favoritos,Planeta_favoritos

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_users():
    users = User.query.all()
    all_users = list(map(lambda item: item.serialize(),users))   
    print(all_users)
    return jsonify(all_users), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_specific_user(user_id):
    person = User.query.get(user_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/user', methods=['POST'])
def post_users():
    request_body_users = request.get_json()   
    new_body = User(email = request_body_users['email'],password = request_body_users['password'],is_active = request_body_users['is_active'])  
    db.session.add(new_body)
    db.session.commit()
    return jsonify("Usuario creado"), 200

@app.route('/people', methods=['GET'])
def handle_people():
    people = People.query.all()
    all_people = list(map(lambda item: item.serialize(), people))
    print(all_people)
    return jsonify(all_people), 200

@app.route('/people', methods=['POST'])
def post_people():
    request_body_people = request.get_json()   
    new_body = People(nombre_persona = request_body_people['nombre_persona'],peso = request_body_people['peso'],color_de_piel = request_body_people['color_de_piel'],color_de_pelo = request_body_people['color_de_pelo'],genero = request_body_people['genero'],birth_year = request_body_people['birth_year'])
    db.session.add(new_body)
    db.session.commit()
    # response_body = {
    #      "msg": "Personaje creado "
    #  }
    return jsonify(request_body_people), 200
    

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_specific_people(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify({'hola'}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    person = People.query.get(people_id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Persona eliminada exitosamente"}), 200
    else:
        return jsonify({"message": "Persona no encontrada"}), 404 


@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda item: item.serialize(), planets))
    print(all_planets)
    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_specific_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def post_planets():
    request_body_planets = request.get_json()   
    new_body = Planets(nombre_planeta = request_body_planets['nombre_planeta'],periodo_rotacion = request_body_planets['periodo_rotacion'],  diametro = request_body_planets['diametro'],clima = request_body_planets['clima'],terreno = request_body_planets['terreno'])
    db.session.add(new_body)
    db.session.commit()
    return jsonify(request_body_planets), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planeta eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Planeta no encontrado"}), 404

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "El usuario no existe"}), 404

    favorites = Favoritos.query.filter_by(usuario_id=user_id).all()
    serialized_favorites = []

    for favorite in favorites:
        serialized_favorite = {
            "id": favorite.id,
            "planeta": favorite.planeta.nombre_planeta,
            "personaje": favorite.nombre.nombre_persona
        }
        serialized_favorites.append(serialized_favorite)

    return jsonify(serialized_favorites), 200

@app.route('/users/<int:user_id>/personajefavoritos', methods=['POST'])
def handle_post_personajefavoritos(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "El usuario no existe"}), 404
    
    request_body_personje = request.get_json()
    new_personjefavorito = Personaje_Favoritos(usuario_id = user_id,people_id = request_body_personje["id"])

    db.session.add(new_personjefavorito)
    db.session.commit()

    return jsonify({"msg":"personaje añadido a favoritos"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)