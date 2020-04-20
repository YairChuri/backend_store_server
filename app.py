from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, UsersList
from resources.item import Item, ItemList
from resources.store import Store, StoreList


'''

https://github.com/jslvtr/rest-api-sections
'''
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # creates /auth

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(UsersList, '/users')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(port=5000)
