from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)
api = Api(app)

# define Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    body = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"Message(title='{self.title}', body='{self.body}')"

with app.app_context():
    db.create_all()

@api.route('/messages')
class MessageResource(Resource):
    def post(self):
        # get authentication token from headers
        auth_token = request.headers.get('Authorization')
        if auth_token != 'secret_token':
            return {'message': 'Unauthorized'}, 401

        # get title and body from request body
        title = request.json['title']
        body = request.json['body']

        existing_message = Message.query.filter_by(title=title).first()
        if existing_message:
            # delete existing message
            db.session.delete(existing_message)
            db.session.commit()

        # create new message object
        new_message = Message(title=title, body=body)
        db.session.add(new_message)
        db.session.commit()
        return {'message': 'Message saved successfully.'}, 201

    def get(self):
        # get title from request parameter
        title = request.args.get('title')
        # retrieve message from database
        message = Message.query.filter_by(title=title).first()
        if message:
            # return message as JSON object
            return {'title': message.title, 'body': message.body}, 200
        else:
            return {'message': 'Message not found.'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

