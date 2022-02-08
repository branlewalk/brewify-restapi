import json
from varname import nameof
from flask import Flask, jsonify, render_template, request
import pymysql
from recipe import recipe, malt, yeast, hops, other

db = pymysql.connect(user='root', passwd='password', host='localhost', database='brewify_db')
cursor = db.cursor()

# Connection String 'mysql+pymysql://db/brew_project'
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False

@app.route('/')
def index():
    pass

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
    cursor.callproc(sproc, params)
    cursor.execute(f'SELECT @_{sproc}_{len(params)-1}')
    result = cursor.fetchone()
    db.commit()
    
    #cursor.close()
    #db.close()

    return result[0]

if __name__ == '__main__':
    app.run(debug=True, port=7099, host='0.0.0.0')