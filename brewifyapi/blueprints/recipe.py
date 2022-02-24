from typing import Text
from flask import jsonify, Blueprint, request, current_app
from brewifyapi import db
from brewifyapi.model.recipe import Recipe, Malt, Yeast, Hop, Other
import json
import pymysql

recipe_blueprint = Blueprint('recipe', __name__)


@recipe_blueprint.route('/', methods=['POST'])
def create_recipe():
    recipe = Recipe(json=request.get_json())
    
    sproc = "sp_store_recipe"
    params = (recipe.recipe_name, recipe.recipe_method, recipe.recipe_srm, recipe.recipe_batch_size,
              recipe.recipe_rating, recipe.recipe_description, recipe.style_id, recipe.image_id,
              recipe.notes_id, recipe.recipe_id)
    
    try:
        recipe_id = db.call_sproc_fetchone(sproc, params)
        if recipe_id is None:
            current_app.logger.warning(f'No recipe with recipe ID: {recipe.recipe_id} was found')
            raise pymysql.MySQLError(f'Unable to find recipe id: {recipe.recipe_id}')
        recipe.recipe_id = recipe_id
        create_recipe_ingredients(recipe)
    except pymysql.MySQLError as e:
        return f'{e}', 400
    return recipe.toJson()

@recipe_blueprint.route('/', methods=['GET'])
def get_recipes():
    sproc = 'sp_get_recipes'
    result = db.call_sproc_fetchall(sproc)
    recipes = map_recipes(result)
    if recipes is None:
        return 'Recipes Not Found', 400
    return json.dumps(recipes, default=lambda o: o.__dict__)

@recipe_blueprint.route('/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    result = db.call_sproc_fetchall(
        'sp_get_recipe', recipe_id)
    recipe = map_recipe(result)
    if recipe is None:
        return f'No recipe found with recipe id: {recipe_id}'
    return recipe.toJson()

@recipe_blueprint.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    result = db.call_sproc_fetchone(
        'sp_remove_recipe_soft', recipe_id)
    return f'Deleted recipe id: {result}'

def map_recipe(db_recipe):
    print(db_recipe)
    if len(db_recipe) != 0:
        recipe = Recipe(db_result=db_recipe[0])
        map_ingredients(recipe)
    else:
        return None
    return recipe
        
def map_recipes(db_recipes):
    recipes = list()
    for db_recipe in db_recipes:
        if db_recipe[8] == 'A':
            recipe = Recipe(db_result=db_recipe)
            map_ingredients(recipe)
            recipes.append(recipe)
    if recipes == None:
        return None
    return recipes

def map_ingredients(recipe):
    malt_result = db.call_sproc_fetchall(
        'sp_get_ingredient_malt', (recipe.recipe_id,)) 
    if malt_result:
        for m in malt_result:
            recipe.malts.append(
                Malt(m[0],m[2],m[3],m[4],m[5],m[6]))
    yeast_result = db.call_sproc_fetchall(
        'sp_get_ingredient_yeast', (recipe.recipe_id,))
    if yeast_result: 
        for y in yeast_result:
            recipe.yeasts.append(
                Yeast(y[0],y[2],y[3],y[4]))
    hop_result = db.call_sproc_fetchall(
        'sp_get_ingredient_hops', (recipe.recipe_id,)) 
    if hop_result:
        for h in hop_result:
            recipe.hops.append(
                Hop(h[0],h[2],h[3],h[4]))
    other_result = db.call_sproc_fetchall(
        'sp_get_ingredient_other', (recipe.recipe_id,)) 
    if other_result:
        for o in other_result:
            recipe.others.append(
                Other(o[0], o[2], o[3]))
        
def create_recipe_ingredients(r):
    try:
        if len(r.malts) > 0:
            for m in r.malts:
                sproc = 'sp_store_ingredient_malt'
                params = (m.malt_id, r.recipe_id, m.malt_ingred_qty, m.malt_ingred_time, m.malt_ingred_type, m.malt_ingred_temp, m.malt_ingred_stage)
                db.call_sproc_fetchone(sproc, params)
    except pymysql.MySQLError as e:
        unable_to_load('malts', r.recipe_id)
    try:
        if len(r.yeasts) > 0:
            for y in r.yeasts:
                sproc = 'sp_store_ingredient_yeast'
                params = (y.yeast_id, r.recipe_id, y.yeast_ingred_qty, y.yeast_ingred_starter, y.yeast_ingred_time)
                db.call_sproc_fetchone(sproc, params)
    except pymysql.MySQLError as e:
        unable_to_load('yeasts', r.recipe_id)
    try:
        if len(r.hops) > 0:
            for h in r.hops:
                sproc = 'sp_store_ingredient_hops'
                params = (h.hops_id, r.recipe_id, h.hops_ingred_qty, h.hops_ingred_time, h.hops_ingred_use)
                db.call_sproc_fetchone(sproc, params)
    except pymysql.MySQLError as e:
        unable_to_load('hops', r.recipe_id)
    try:
        if len(r.others) > 0:
            for o in r.others:
                sproc = 'sp_store_ingredient_other'
                params = (o.other_id, r.recipe_id, o.other_ingred_qty, o.other_ingred_time)
                db.call_sproc_fetchone(sproc, params)
    except pymysql.MySQLError as e:
        unable_to_load('others', r.recipe_id)
    
def unable_to_load(name, recipe_id):
    delete_recipe_hard(recipe_id)
    raise pymysql.MySQLError(f'Unable to load {name}, rolling back recipe')

def delete_recipe_hard(recipe_id):
    sproc = 'sp_remove_recipe_hard'
    db.call_sproc_fetchone(sproc, [recipe_id])
