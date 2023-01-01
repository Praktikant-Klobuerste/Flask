from flask import Flask, jsonify, render_template, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app import Cafe, cafe_information
import random




index_bp = Blueprint('Index', __name__, "Handles Starting Page")
bp = Blueprint('Cafe', __name__, "Operations on cafes")

@index_bp.route('/')
def home():
    return render_template("index.html")



@bp.route("/random")
def random_cafe():
    ## HTTP GET - Read Record
    cafes = Cafe.query.all()
    random_cafe = random.choice(cafes)

    cafe_json = jsonify(cafe = cafe_information(random_cafe).json)


    return cafe_json