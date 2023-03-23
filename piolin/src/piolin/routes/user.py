from flask import request
from flask_restful import Resource, reqparse
from piolin.db import db
from piolin.models.user import User
from piolin.routes.utils import verify_token

class UserAPI(Resource):
    # create a new user
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nickname', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        # check if user already exists
        user = User.query.filter_by(nickname=args['nickname']).first()
        if user is not None:
            return {'message': 'User already exists'}, 409

        # create new user and add to database
        new_user = User(nickname=args['nickname'], password=args['password'], email=args['email'], name=args['name'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    # update an existing user
    def put(self):
        user = verify_token(request)
        if not user:
            return {'message': 'Unauthorized'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=False)
        parser.add_argument('name', type=str, required=False)
        args = parser.parse_args()

        # check if user exists
        dbUser = User.query.filter_by(nickname=user).first()
        if dbUser is None:
            return {'message': 'User not found'}, 404

        # update user email and name if provided
        if args['email']:
            dbUser.email = args['email']
        if args['name']:
            dbUser.name = args['name']
        if args['password']:
            dbUser.password = args['password']
        db.session.commit()

        return {'message': 'User updated successfully'}, 200
