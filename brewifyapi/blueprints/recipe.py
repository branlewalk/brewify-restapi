from flask import jsonify, Blueprint, request, current_app
from brewifyapi import db
from brewifyapi.model.recipe import recipe



# Recipe Blueprint
recipe_blueprint = Blueprint('recipe', __name__)

# Recipe Routes (Create, Read/Read All, Update, Delete)
@recipe_blueprint.route('/', methods=['POST'])
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
    
    r.recipe_id = db.call_stored_procedure(sproc, params)
    
    #create_recipe_ingredients(r)
    
    return r.toJson()

def create_recipe_ingredients(r):
    if len(r.malts) > 0:
        for m in r.malts:
            sproc = 'sp_create_malt_ingredient'
            params = (r.recipe_id, m.malt_id, m.malt_ingred_qty, m.malt_ingred_time, m.malt_ingred_type, m.malt_ingred_temp, m.malt_ingred_stage)
            db.call_stored_procedure(sproc, params)
    if len(r.yeasts) > 0:
        for y in r.yeasts:
            sproc = 'sp_create_yeast_ingredient'
            params = (r.recipe_id, y.yeast_id, y.yeast_ingred_qty, y.yeast_ingred_starter, y.yeast_ingred_time)
            db.call_stored_procedure(sproc, params)
    if len(r.hops) > 0:
        for h in r.hops:
            sproc = 'sp_create_hops_ingredient'
            params = (r.recipe_id, h.hops_id, h.hops_ingred_qty, h.hops_ingred_time, h.hops_ingred_use)
            db.call_stored_procedure(sproc, params)
    if len(r.others) > 0:
        for o in r.others:
            sproc = 'sp_create_other_ingredient'
            params = (r.recipe_id, o.other_id, o.other_ingred_qty, o.other_ingred_time)
            db.call_stored_procedure(sproc, params)