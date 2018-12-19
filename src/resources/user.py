import sqlite3
from flask_restful import Resource, request, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="Username cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Password cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with this username already exists"}, 400

        # user = UserModel(data["username"], data["password"])
        user = UserModel(**data)
        user.save_to_db()

        # 201 resource created
        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not Found."}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not Found."}
        user.delete_from_db()
        return {"message": "User deleted."}, 200
