from flask import Flask
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    api = Api(app)

    # load configuration settings
    app.config.from_object('piolin.config.Config')

    # initialize database
    from piolin.db import init_db
    from piolin.models import Message
    from piolin.models import Tweet
    from piolin.models import User
    init_db(app)

    from piolin.routes.user import UserAPI
    from piolin.routes.tweet import TweetAPI
    from piolin.routes.message import MessageAPI
    from piolin.routes.messagestream import MessageStreamAPI
    api.add_resource(UserAPI, '/users')
    api.add_resource(TweetAPI, '/tweets', '/tweets/<string:nickname>')
    api.add_resource(MessageAPI, '/messages')
    api.add_resource(MessageStreamAPI, '/messages-stream')

    return app
