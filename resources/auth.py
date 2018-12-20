from flask_restful import Resource, request


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
