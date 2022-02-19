from flask import jsonify, Blueprint, request, current_app
from brewifyapi import db
from brewifyapi.model.recipe import Recipe, Recipes, Malt, Yeast, Hop, Other
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
    
    recipe.recipe_id = db.call_sproc_fetchone(sproc, params)
    create_recipe_ingredients(recipe)
    
    return recipe.toJson()

@recipe_blueprint.route('/', methods=['GET'])
def get_recipes():
    sproc = 'sp_get_recipes'
    result = db.call_sproc_fetchall(sproc)
    recipes = map_recipes(result)
    return recipes.toJson()

@recipe_blueprint.route('/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    sproc = 'sp_get_recipe'
    result = db.call_sproc_fetchall(sproc, recipe_id)
    recipe = map_recipe(result)
    return recipe.toJson()

def map_recipe(db_recipe):
    print(f'recipe from db: {db_recipe}')
    if db_recipe[0][8] == 'A':
        recipe = Recipe(db_result=db_recipe[0])
        map_ingredients(recipe)
    if recipe == None:
        return 'BadRequest'
    return recipe
        
def map_recipes(db_recipes):
    recipes = Recipes()
    for db_recipe in db_recipes:
        if db_recipe[8] == 'A':
            recipe = Recipe(db_result=db_recipe)
            map_ingredients(recipe)
            recipes.recipes.append(recipe)
    if recipes == None:
        return 'BadRequest'
    return recipes    

def map_ingredients(recipe):
    malt_result = db.call_sproc_fetchall('sp_get_ingredient_malt', (recipe.recipe_id,)) 
    if malt_result:
        for m in malt_result:
            print(m)
            recipe.malts.append(Malt(m[0],m[2],m[3],m[4],m[5],m[6]))
    yeast_result = db.call_sproc_fetchall('sp_get_ingredient_yeast', (recipe.recipe_id,))
    if yeast_result: 
        for y in yeast_result:
            print(y)
            recipe.yeasts.append(Yeast(y[0],y[2],y[3],y[4]))
    hop_result = db.call_sproc_fetchall('sp_get_ingredient_hops', (recipe.recipe_id,)) 
    if hop_result:
        for h in hop_result:
            print(h)
            recipe.hops.append(Hop(h[0],h[2],h[3],h[4]))
    other_result = db.call_sproc_fetchall('sp_get_ingredient_other', (recipe.recipe_id,)) 
    if other_result:
        for o in other_result:
            print(o)
            recipe.others.append(Other(o[0], o[2], o[3]))
        
def create_recipe_ingredients(r):
    if len(r.malts) > 0:
        for m in r.malts:
            sproc = 'sp_store_ingredient_malt'
            params = (m.malt_id, r.recipe_id, m.malt_ingred_qty, m.malt_ingred_time, m.malt_ingred_type, m.malt_ingred_temp, m.malt_ingred_stage)
            db.call_sproc_fetchone(sproc, params)
    if len(r.yeasts) > 0:
        for y in r.yeasts:
            sproc = 'sp_store_ingredient_yeast'
            params = (y.yeast_id, r.recipe_id, y.yeast_ingred_qty, y.yeast_ingred_starter, y.yeast_ingred_time)
            db.call_sproc_fetchone(sproc, params)
    if len(r.hops) > 0:
        for h in r.hops:
            sproc = 'sp_store_ingredient_hops'
            params = (h.hops_id, r.recipe_id, h.hops_ingred_qty, h.hops_ingred_time, h.hops_ingred_use)
            db.call_sproc_fetchone(sproc, params)
    if len(r.others) > 0:
        for o in r.others:
            sproc = 'sp_store_ingredient_other'
            params = (o.other_id, r.recipe_id, o.other_ingred_qty, o.other_ingred_time)
            db.call_sproc_fetchone(sproc, params)