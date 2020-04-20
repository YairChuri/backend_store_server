
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class ItemList(Resource):

    def get(self):
        items = ItemModel.get_all_items()
        return {'items': [item.json() for item in items]}, 200


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': 'Item not found.'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': 'Item already exist.'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "Internal error while inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        http_code = 200
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            http_code = 201
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(), http_code
