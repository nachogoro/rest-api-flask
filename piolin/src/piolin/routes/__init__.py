from flask import Blueprint

# define blueprints for each module
user_bp = Blueprint('user', __name__)
tweet_bp = Blueprint('tweet', __name__)
message_bp = Blueprint('message', __name__)

# import endpoints from each module
from piolin.routes.user import *
from piolin.routes.tweet import *
from piolin.routes.message import *

