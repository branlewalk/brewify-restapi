import os
from varname import nameof
from flask import Flask, jsonify, render_template, request
from brewifyapi.database import Database
from brewifyapi.model.recipe import recipe, malt, yeast, hops, other
import brewifyapi

db = Database()

def create_app(config_env='DevConfig'):
    app = Flask(__name__)
    app.config.from_object(f'brewifyapi.config.{config_env}')  

    db.init_app(app)
    
    @app.route('/', methods=['GET'])
    def index():
        return 'No entries here so far'

    @app.route('/recipes', methods=['POST'])
    def create_recipe():
        r = recipe(request.get_json())

        print(f'recipe id is \'{r.recipe_id}\'')
        
        sproc = "sp_store_recipe"
        params = (r.recipe_name, 
                r.recipe_method,
                r.recipe_srm,
                r.recipe_batch_size,
                r.recipe_rating,
                r.recipe_description,
                r.style_id,
                r.image_id,
                r.notes_id,
                r.recipe_id)
        
        r.recipe_id = call_stored_procedure(sproc, params)
        
        #create_recipe_ingredients(r)
        
        return r.toJson()
        
    @app.route('/session')
    def session():
        pass

    @app.route('/ingredients')
    def ingredients():
        pass

    def create_recipe_ingredients(r):
        if len(r.malts) > 0:
            for m in r.malts:
                sproc = 'sp_create_malt_ingredient'
                params = (r.recipe_id, m.malt_id, m.malt_ingred_qty, m.malt_ingred_time, m.malt_ingred_type, m.malt_ingred_temp, m.malt_ingred_stage)
                call_stored_procedure(sproc, params)
        if len(r.yeasts) > 0:
            for y in r.yeasts:
                sproc = 'sp_create_yeast_ingredient'
                params = (r.recipe_id, y.yeast_id, y.yeast_ingred_qty, y.yeast_ingred_starter, y.yeast_ingred_time)
                call_stored_procedure(sproc, params)
        if len(r.hops) > 0:
            for h in r.hops:
                sproc = 'sp_create_hops_ingredient'
                params = (r.recipe_id, h.hops_id, h.hops_ingred_qty, h.hops_ingred_time, h.hops_ingred_use)
                call_stored_procedure(sproc, params)
        if len(r.others) > 0:
            for o in r.others:
                sproc = 'sp_create_other_ingredient'
                params = (r.recipe_id, o.other_id, o.other_ingred_qty, o.other_ingred_time)
                call_stored_procedure(sproc, params)

    def call_stored_procedure(sproc, params):
        db.open_connection()
        cursor = db.conn.cursor()
        cursor.callproc(sproc, params)
        cursor.execute(f'SELECT @_{sproc}_{len(params)-1}')
        result = cursor.fetchone()
        db.conn.commit()
        return result[0]
    
    return app