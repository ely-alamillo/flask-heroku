import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="Price cannot be blank."
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="every item needs a\
        store_id.",
    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            # 400 bad request
            return (
                {
                    "message": "An item with name '{}' already exists".format(
                        name
                    )
                },
                400,
            )

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            # 500 internal server error, not your fault ours
            return {"message": "an error occured inserting the item"}, 500

        # 201 is for created
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()

        if not claims["is_admin"]:
            return {"message": "Admin privilege required"}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "item deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            # change store_id ?
            item.price = data["price"]
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.find_all()]
        # items = [item.json() for item in ItemModel.query.all()]
        # items = list(map(lambda x: x.json(), ItemModel.query.all()))
        return {"items": items}