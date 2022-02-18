from flask import jsonify, Blueprint, request, current_app
from brewifyapi import db
from brewifyapi.model.recipe import Recipe, Recipes
import asyncio

# Recipe Blueprint
recipe_blueprint = Blueprint('recipe', __name__)

# Recipe Routes (Create, Read/Read All, Update, Delete)
@recipe_blueprint.route('/', methods=['POST'])
def create_recipe():
    recipe = Recipe(json=request.get_json())
    
    sproc = "sp_store_recipe"
    params = (recipe.recipe_name, recipe.recipe_method, recipe.recipe_srm, recipe.recipe_batch_size,
              recipe.recipe_rating, recipe.recipe_description, recipe.style_id, recipe.image_id,
              recipe.notes_id, recipe.recipe_id)
    
    recipe.recipe_id = db.call_sproc(sproc, params)
    create_recipe_ingredients(recipe)
    
    return recipe.toJson()

@recipe_blueprint.route('/', methods=['GET'])
def get_recipes():
    sproc = 'sp_get_recipes'
    result = db.call_get_sproc(sproc)
    recipes = map_recipe(result)
    # Get the ingredients
    return recipes.toJson()

def map_recipe(db_recipes):
    recipes = Recipes()
    for db_recipe in db_recipes:
        if db_recipe[8] == 'A':
            recipes.recipes.append(Recipe(db_result=db_recipe))
    return recipes    
        
    
def create_recipe_ingredients(r):
    if len(r.malts) > 0:
        for m in r.malts:
            sproc = 'sp_store_ingredient_malt'
            params = (m.malt_id, r.recipe_id, m.malt_ingred_qty, m.malt_ingred_time, m.malt_ingred_type, m.malt_ingred_temp, m.malt_ingred_stage)
            db.call_sproc(sproc, params)
    if len(r.yeasts) > 0:
        for y in r.yeasts:
            sproc = 'sp_store_ingredient_yeast'
            params = (y.yeast_id, r.recipe_id, y.yeast_ingred_qty, y.yeast_ingred_starter, y.yeast_ingred_time)
            db.call_sproc(sproc, params)
    if len(r.hops) > 0:
        for h in r.hops:
            sproc = 'sp_store_ingredient_hops'
            params = (h.hops_id, r.recipe_id, h.hops_ingred_qty, h.hops_ingred_time, h.hops_ingred_use)
            db.call_sproc(sproc, params)
    if len(r.others) > 0:
        for o in r.others:
            sproc = 'sp_store_ingredient_other'
            params = (o.other_id, r.recipe_id, o.other_ingred_qty, o.other_ingred_time)
            db.call_sproc(sproc, params)