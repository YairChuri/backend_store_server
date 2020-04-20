from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'message': 'Store not found.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store {name} with this name already exists.'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': f'Failed to create store {name}.'}, 500
        return store.json(), 201

    def delete(self, name):
        if StoreModel.find_by_name(name):
            return 200

        store = StoreModel(name)
        try:
            store.delete_from_db()
        except:
            return {'message': f'Failed to delete store {name}.'}, 500
        return {'message': f'Store {name} deleted.'}, 200


class StoreList(Resource):

    def get(self):
        stores = StoreModel.get_all_stores()
        return {'stores': [store.json() for store in stores]}
