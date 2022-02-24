import json
import os
from varname import nameof
from flask import Flask, jsonify, render_template, request
from brewifyapi.database import Database

db = Database()

def create_app(config_env='DevConfig'):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(f'brewifyapi.config.{config_env}')  
    app.app_context()
    
    db.init_app(app)
    
    from brewifyapi.blueprints.recipe import recipe_blueprint
    app.register_blueprint(recipe_blueprint, url_prefix='/recipe')
    
    @app.route('/', methods=['GET'])
    def index():
        return 'No entries here so far'
    
    return app