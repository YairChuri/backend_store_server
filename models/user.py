#import sqlite3
from database import db


class UserModel(db.Model):
    '''
    A few words on resources and models: 
    1. The user model is out internal representation of the data. The API doesn't interact with the model directly 
    it access the resources. 
    2. The model is essentially a collection of helper function that allows us to interact 
    with the database. 
    3. It creates a separation between what the client sees and the internal of the application. 
    4. The resource is using the model not the other way around. 
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _username, _password):
        self.username = _username
        self.password = _password

    def json(self):
        return {'username': self.username, 'password': self.password}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
