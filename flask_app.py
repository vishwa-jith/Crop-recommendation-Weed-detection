from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from numpy.core.numeric import full
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import numpy as np
import pandas as pd
from flask_cors import CORS, cross_origin


from api import weatherApi
from utils import utils

app = Flask(__name__)
app.config['SECRET_KEY'] = '0123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
CORS(app, support_credentials=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    full_name = db.Column(db.String(80))
    state_name = db.Column(db.String(50))
    district_name = db.Column(db.String(50))
    area = db.Column(db.Integer)
    soil_type = db.Column(db.String(60))
    mobile = db.Column(db.String(60))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            return jsonify({
                'message': 'Token is invalid'
            }), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def getUserProfile(current_user):
    return jsonify({"username": current_user.username, "password": current_user.password, "full_name": current_user.full_name, "state_name": current_user.state_name, "district_name": current_user.district_name, "area": current_user.area, "soil_type": current_user.soil_type, "mobile": current_user.mobile})


@app.route('/user/update', methods=['PUT'])
@token_required
def updateUserProfile(current_user):
    updateUser = request.json
    user = User.query.filter_by(id=current_user.id).first()
    userUsername = User.query.filter_by(
        username=updateUser.get('username')).first()
    if current_user.username != updateUser.get('username'):
        if not userUsername:
            user.username = updateUser.get('username')
        else:
            return make_response(jsonify({"message": "Username already taken."}), 400)
    user.full_name = updateUser.get('full_name')
    user.state_name = updateUser.get('state_name')
    user.district_name = updateUser.get('district_name')
    user.area = updateUser.get('area')
    user.soil_type = updateUser.get('soil_type')
    user.mobile = updateUser.get('mobile')
    db.session.commit()
    return jsonify({"message": "User Profile updated successfully"})


@app.route('/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            jsonify({"message": "Could not verify"}),
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required"'}
        )

    user = User.query.filter_by(username=auth.get('username')).first()

    if not user:
        return make_response(
            jsonify({"message": "Username doesn't exist"}),
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({"message": "Login Sucessful", 'token': token.decode("UTF-8")}), 201)
    return make_response(
        jsonify({"message": "Wrong username or password"}),
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(
            public_id=str(uuid.uuid4()),
            username=username,
            password=generate_password_hash(password),
            full_name=full_name
        )
        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({"success": True, "message": "Sucessfully Registered"}), 201)
    else:
        return make_response(jsonify({"success": False, "message": 'User already exists. Please Log in'}), 202)


@app.route("/A1/recommendCrop", methods=['GET'])
def recommendCrop1():
    district = request.args.get("district")
    weather = np.array(weatherApi.getWeather(district)).reshape(1, -1)
    cropRecommendationApproach1 = utils.loadpickles(
        "pickledFiles/cropRecommendationA1.pkl")
    crop = cropRecommendationApproach1.predict(weather)
    return jsonify({"crop": crop[0]})


@app.route("/A1/recommendNPK", methods=['POST'])
def recommendNPK():
    NPKPrediction = pd.read_csv(
        "./preprocessedData/CropRecommentationApproach2.csv")
    NPKPrediction = NPKPrediction[NPKPrediction['N'] > 0 &
                                  NPKPrediction['P'] & NPKPrediction['K']].reset_index(drop=True)
    category = list(dict(
        enumerate(NPKPrediction['label'].astype('category').cat.categories)).values())

    data = request.json
    crop = category.index(data.get("crop"))

    district = request.args.get("district")
    weather = weatherApi.getWeather(district)
    nitrogen = utils.loadpickles(
        "pickledFiles/predictNitrogen.pkl")
    nitrogen_input = np.array([*weather, crop]).reshape(1, -1)
    nitrogen_level = nitrogen.predict(nitrogen_input)
    print(nitrogen_input)
    phosphorus = utils.loadpickles(
        "pickledFiles/predictPhosphorus.pkl")
    phosphorus_input = np.array([*weather, crop]).reshape(1, -1)
    phosphorus_level = phosphorus.predict(phosphorus_input)

    potassium = utils.loadpickles(
        "pickledFiles/predictPotassium.pkl")
    potassium_input = np.array([*weather, crop]).reshape(1, -1)
    potassium_level = potassium.predict(potassium_input)

    return jsonify({"nitrogen": nitrogen_level[0], "phosphorus": phosphorus_level[0], "potassium": potassium_level[0]})


@app.route("/A1/recommendFertilizer", methods=['POST'])
def recommendFertilizer():
    data = request.json

    NPKPrediction = pd.read_csv(
        "./data/FertilizerPrediction.csv")
    crop_category = list(dict(
        enumerate(NPKPrediction['Crop Type'].astype('category').cat.categories)).values())
    soil_category = list(dict(
        enumerate(NPKPrediction['Soil Type'].astype('category').cat.categories)).values())
    fertilizer_category = dict(
        enumerate(NPKPrediction['Fertilizer Name'].astype('category').cat.categories))

    soil = soil_category.index(data.get('soil'))
    crop = crop_category.index(data.get('crop'))
    nitrogen = data.get('nitrogen')
    potassium = data.get('potassium')
    phosphorus = data.get('phosphorus')

    district = request.args.get("district")
    weather = weatherApi.getWeather(district)[:2]
    fertilizerRecommendation = utils.loadpickles(
        "pickledFiles/fertilizerRecommendation.pkl")
    fertilizer_input = np.array(
        [*weather,  soil, crop, nitrogen, potassium, phosphorus]).reshape(1, -1)
    fertilizer = fertilizerRecommendation.predict(fertilizer_input)
    fertilizer = fertilizer_category[fertilizer[0]]
    return jsonify({"fertilizer": fertilizer})


@app.route("/A2/recommendCrop", methods=['POST'])
def recommendCrop2():
    data = request.json

    nitrogen = data.get('nitrogen')
    phosphorus = data.get('phosphorus')
    potassium = data.get('potassium')

    district = request.args.get("district")
    weather = weatherApi.getWeather(district)
    cropRecommendationApproach2 = utils.loadpickles(
        "pickledFiles/cropRecommendationA2.pkl")
    crop_input = np.array(
        [nitrogen, phosphorus, potassium, *weather]).reshape(1, -1)
    crop = cropRecommendationApproach2.predict(crop_input)
    return jsonify({"crop": crop[0]})


@app.route("/recommendCropYield", methods=['POST'])
def recommendCropYield():
    data = request.json
    crop = data.get('crop')
    area = data.get('area')

    CropProduction = pd.read_csv(
        "./data/CropProductionMinified.csv")
    CropProduction = CropProduction[CropProduction['Production'] > 0].reset_index(
        drop=True)

    crop_category = list(dict(
        enumerate(CropProduction['Crop'].astype('category').cat.categories)).values())
    crop = crop_category.index(crop)

    args = request.args
    state = args.get("state")
    district = args.get("district")
    season = args.get("season")
    season = season if season else utils.getSeason()

    state_category = list(dict(
        enumerate(CropProduction['State_Name'].astype('category').cat.categories)).values())
    district_category = list(dict(
        enumerate(CropProduction['District_Name'].astype('category').cat.categories)).values())
    season_category = ['Autumn', 'Kharif',
                       'Rabi', 'Summer', 'Whole Year', 'Winter']

    state = state_category.index(state)
    district = district_category.index(district)
    season = season_category.index(season)

    cropProduction = utils.loadpickles(
        "pickledFiles/cropProduction.pkl")
    yield_input = np.array(
        [state, district, season, crop, area]).reshape(1, -1)

    cropProductionScaler = utils.loadpickles(
        "pickledFiles/cropProductionScaler.sav")
    yield_input_scaler = cropProductionScaler.transform(yield_input)
    crop_yield = cropProduction.predict(yield_input_scaler)
    return jsonify({"yield": crop_yield[0]})


@app.route("/states", methods=['GET'])
@token_required
def getStates(current_user):
    CropProduction = pd.read_csv(
        "./data/CropProductionMinified.csv")
    CropProduction = CropProduction[CropProduction['Production'] > 0].reset_index(
        drop=True)

    state_category = dict(
        enumerate(CropProduction['State_Name'].astype('category').cat.categories))
    return jsonify(state_category)


@app.route("/districts", methods=['GET'])
@token_required
def getDistricts(current_user):
    args = request.args
    state = args.get("state_name")
    CropProduction = pd.read_csv(
        "./data/CropProductionMinified.csv")
    CropProduction = CropProduction[CropProduction['Production'] > 0].reset_index(
        drop=True)

    district_category = dict(
        enumerate(CropProduction[CropProduction['State_Name'] == state]['District_Name'].astype('category').cat.categories))
    return jsonify(district_category)


@app.route("/crops", methods=['GET'])
def getCrops():
    CropProduction = pd.read_csv(
        "./data/CropProductionMinified.csv")
    CropProduction = CropProduction[CropProduction['Production'] > 0].reset_index(
        drop=True)

    crops_category = dict(
        enumerate(CropProduction['Crop'].astype('category').cat.categories))
    return jsonify(crops_category)


@app.route("/seasons", methods=['GET'])
def getSeasons():
    CropProduction = pd.read_csv(
        "./data/CropProductionMinified.csv")
    CropProduction = CropProduction[CropProduction['Production'] > 0].reset_index(
        drop=True)

    season_category = dict(
        enumerate(CropProduction['Season'].astype('category').cat.categories))
    return jsonify(season_category)


@app.route("/soils", methods=['GET'])
@token_required
def getSoils(current_user):
    FertilizerPrediction = pd.read_csv(
        "./data/FertilizerPrediction.csv")
    soil_category = dict(
        enumerate(FertilizerPrediction['Soil Type'].astype('category').cat.categories))
    return jsonify(soil_category)


@app.route("/weather", methods=['GET'])
@token_required
def getWeather(current_user):
    args = request.args
    district = args.get("district_name")
    weather = np.array(weatherApi.getWeather(district))
    return jsonify({"temperature": weather[0], "humidity": weather[1], "rainfall": weather[2]})


if __name__ == "__main__":
    app.run(debug=True)
