import json
import pytest

from brewifyapi import create_app, db

@pytest.fixture
def client():
    app = create_app('TestConfig')

    with app.test_client() as client:
        with app.app_context():
            db.open_connection()
        yield client
        
@pytest.fixture
def recipe_data():
    recipe = {
    "recipe_id" : "",
    "recipe_name": "Another Recipe", 
    "recipe_method" : "All-Grain", 
    "recipe_srm" : "10", 
    "recipe_batch_size" : "20",
    "recipe_rating" : "3",
    "recipe_description" : "Second Recipe",
    "style_id" : "2",
    "image_id" : "2",
    "ingredients" : {
        "malt" : [
            {
                "malt_id" : "15",
                "malt_ingred_qty" : "15.5",
                "malt_ingred_time" : "60",
                "malt_ingred_type" : "Wort",
                "malt_ingred_temp" : "148.2",
                "malt_ingred_stage" : "Infusion Step 1"
            }
        ],
        "yeast" : [
            {
                "yeast_id" : "42",
                "yeast_ingred_qty" : "1",
                "yeast_ingred_starter" : "true",
                "yeast_ingred_time" : "14"
            }
        ],
        "hops" : [
            {
                "hops_id" : "2",
                "hops_ingred_qty" : "2",
                "hops_ingred_time" : "15",
                "hops_ingred_use" : "Boil"
            }
        ]
    }
}  
    return json.dumps(recipe)