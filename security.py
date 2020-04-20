from werkzeug.security import safe_str_cmp
from resources.user import UserModel


# this method is called when the user is calling /auth endpoint with provided
# username and password. if an authenticated user is returned, flask-jwt generated
# a jwt token that is returned to the client to be used with any subsequent API
# calls. The jwt token expires in 5 minutes by default.
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

# this method is called with each API call carring the jwt token
# to authenticate the token and associate it with a known user id


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
