from security import authenticate, identity
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

# from flask_jwt import JWT, jwt_required
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["JWT_SECRET_KEY"] = "secretkeyboyz"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


class Auth(Resource):
    def post(self):
        if not request.is_json:
            return {"message": "request malformed."}, 400

        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username:
            return {"message": "Missing username"}, 400

        if not password:
            return {"message": "Missing password"}, 400

        user = authenticate(username, password)

        if not user:
            return {"message": "invalid login credentials"}, 401

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200


api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(Auth, "/auth")

if __name__ == "__main__":
    from db import db

    # set up db
    db.init_app(app)
    app.run(port=5000, debug=True)
