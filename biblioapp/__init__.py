from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

# Initialize app, db, and api at the module level
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
api = Api(
    app,
    authorizations={
        'BearerAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter your Bearer token in the format **Bearer <token>**'
        }
    },
    security='BearerAuth',
    doc='/api/v1'
)

# Define namespace and register routes
v1 = api.namespace('api/v1', description='Version 1 of the API')

# Register the API routes
from .resources import register_routes
register_routes(v1)
api.add_namespace(v1)

