from flask import Flask, jsonify
import os

from .ext import configuration

def get_base_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    template_dir = os.path.abspath('app/templates')
    static_dir = os.path.abspath('app/static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    configuration.init_app(app)

    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({
            'error': 'Bad Request',
            'message': error.description
        })
        response.status_code = 400
        return response

    return app


app = create_app()