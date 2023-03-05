from flask import Flask, Response
from flask_restful import Api, Resource
import time

app = Flask(__name__)
api = Api(app)

class StreamData(Resource):
    def get(self):
        def generate():
            yield '{"title": "Cabecera"}\n'
            time.sleep(1)
            yield '{"title": "Cuerpo"}\n'
            time.sleep(1)
            yield '{"title": "Final"}\n'

        return Response(generate(), mimetype='application/x-ndjson')

api.add_resource(StreamData, '/stream-data')

if __name__ == '__main__':
    app.run(debug=True)
