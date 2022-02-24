import json
    
def test_index_route(client):
    response = client.get('/')
    assert b'No entries here so far' in response.data
    
def test_recipe_post(client, recipe_data):
    response = client.post('/recipe/', 
                           data=recipe_data,
                           headers={"Content-Type": "application/json"})
    
    data = json.loads(response.data)
    assert data['recipe_name'] in 'Another Recipe'
    assert data['recipe_method'] in 'All-Grain'
    assert data['recipe_srm'] == 10
    assert data['recipe_batch_size'] == 20
    assert data['recipe_rating'] == 3
    assert data['recipe_description'] in 'Second Recipe'
    assert data['style_id'] == 2
    assert data['image_id'] == 2
    
def test_recipe_delete(client):
    response = client.delete('recipe/1')
    assert response.message is 'deleted something'
    
 