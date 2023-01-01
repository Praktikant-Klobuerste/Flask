from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from distutils.util import strtobool

from flask_smorest import Api
from cafe import index_bp as IndexBlueprint
from cafe import bp as CafeBlueprint


app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = "Coffee API"
app.config['API_VERSION'] = "v1"
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
api.register_blueprint(IndexBlueprint)
api.register_blueprint(CafeBlueprint)




# ##Cafe TABLE Configuration
# class Cafe(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), unique=True, nullable=False)
#     map_url = db.Column(db.String(500), nullable=False)
#     img_url = db.Column(db.String(500), nullable=False)
#     location = db.Column(db.String(250), nullable=False)
#     seats = db.Column(db.String(250), nullable=False)
#     has_toilet = db.Column(db.Boolean, nullable=False)
#     has_wifi = db.Column(db.Boolean, nullable=False)
#     has_sockets = db.Column(db.Boolean, nullable=False)
#     can_take_calls = db.Column(db.Boolean, nullable=False)
#     coffee_price = db.Column(db.String(250), nullable=True)



def cafe_information(_cafe):
    
    return jsonify(
        id = _cafe.id,
        name = _cafe.name,
        map_url = _cafe.map_url,
        img_url = _cafe.img_url,
        location = _cafe.location,
        seats = _cafe.seats,
        has_toilet = _cafe.has_toilet,
        has_wifi = _cafe.has_wifi,
        has_sockets = _cafe.has_sockets,
        can_take_calls = _cafe.can_take_calls,
        coffee_price = _cafe.coffee_price,
    )



# @app.route("/random")
# def random_cafe():
#     ## HTTP GET - Read Record
#     cafes = Cafe.query.all()
#     random_cafe = random.choice(cafes)

#     cafe_json = jsonify(cafe = cafe_information(random_cafe).json)


#     return cafe_json


@app.route("/all")
def all_cafes():
    cafes = Cafe.query.all()
    all_cafes_list = []
    for cafe in cafes:
        cafe_json = cafe_information(cafe).json
        all_cafes_list.append(cafe_json)

    return jsonify(cafes = all_cafes_list)


@app.route("/search")
def find_cafe():
    searchword = request.args.get("loc")
    cafe = Cafe.query.filter_by(location = searchword).first()
    print(cafe)
    if cafe:
        return cafe_information(cafe)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
    

## HTTP POST - Create Record
@app.route("/add", methods = ["POST"])
def add_cafe():
    print(request.form)
    # print(request.get_json())
    print(bool(strtobool(request.form.get("has_toilet"))))
    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get("map_url"),
        img_url = request.form.get("img_url"),
        location = request.form.get("location"),
        seats = request.form.get("seats"),
        has_toilet = bool(strtobool(request.form.get("has_toilet"))),
        has_wifi = bool(strtobool(request.form.get("has_wifi"))),
        has_sockets = bool(strtobool(request.form.get("has_sockets"))),
        can_take_calls = bool(strtobool(request.form.get("can_take_calls"))),
        coffee_price = request.form.get("coffee_price")
                )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(
            response = jsonify(success = f"Successfully added the new cafe: {new_cafe.name}.").json
            )


            


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods = ["PATCH"])
def update_price(cafe_id):
    cafe = Cafe.query.filter_by(id = cafe_id).first()

    if cafe:
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(
                response = jsonify(success = f"[{cafe_id}] - Successfully updated the price of {cafe.name} to {cafe.coffee_price}.").json
        )

    else: 
        return jsonify(error = {"Not found" : f'Sorry a cafe with id-{cafe_id} was not found in the database.'}), 404

    


## HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods = ["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    cafe = Cafe.query.filter_by(id = cafe_id).first()

    if cafe:
        if api_key == "TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(
                success = jsonify(f"Deleted Cafe: {cafe.name}").json)
        else:
            return jsonify(error = "Sorry, that's not allowed. Make sure you have the correct api-key."), 403
    else:
        return jsonify(error = {"Not found" : f'Sorry a cafe with id-{cafe_id} was not found in the database.'}), 404
    




if __name__ == '__main__':
    app.run(debug=True)
