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

    sproc = "CreateRecipe"
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
    
    create_recipe_ingredients(r)
    
    return jsonify(r)
    
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
            params = (m.malt_id, )
            
            

def call_stored_procedure(sproc, params):
    cursor.callproc(sproc, params)
    cursor.execute(f'SELECT @_{sproc}_{len(params)-1}')
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result[0]

if __name__ == '__main__':
    app.run(debug=True, port=7099, host='0.0.0.0')