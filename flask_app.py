from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import numpy as np

from api import weatherApi
from utils import utils

app = Flask(__name__)
app.config['SECRET_KEY'] = '0123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'public_id': user.public_id,
            'username': user.username,
        })
    return jsonify({'users': output})


@app.route('/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query.filter_by(username=auth.get('username')).first()

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode("UTF-8")}), 201)
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(
            public_id=str(uuid.uuid4()),
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists. Please Log in.', 202)


@app.route("/A1/recommendCrop", methods=['GET'])
def recommendCrop1():
    district = request.args.get("district")
    weather = np.array(weatherApi.getWeather(
        district if district else "Bangalore")).reshape(1, -1)
    cropRecommendationApproach1 = utils.loadpickles(
        "pickledFiles/cropRecommendationA1.pkl")
    crop = cropRecommendationApproach1.predict(weather)
    print(district)
    return jsonify({"crop": crop[0]})


@app.route("/A2/recommendCrop", methods=['POST'])
def recommendCrop2():
    data = request.json

    nitrogen = data.get('nitrogen')
    phosphorus = data.get('phosphorus')
    potassium = data.get('potassium')

    district = request.args.get("district")
    weather = weatherApi.getWeather(district if district else "Bangalore")
    cropRecommendationApproach2 = utils.loadpickles(
        "pickledFiles/cropRecommendationA2.pkl")
    crop_input = np.array(
        [nitrogen, phosphorus, potassium, *weather]).reshape(1, -1)
    crop = cropRecommendationApproach2.predict(crop_input)
    return jsonify({"crop": crop[0]})


if __name__ == "__main__":
    app.run(debug=True)
