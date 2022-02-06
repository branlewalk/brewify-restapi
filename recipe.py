class recipe:
    
    def __init__(self, json):
        self.recipe_id = json["recipe_id"] if 'recipe_id' in json else None
        self.recipe_name = json["recipe_name"] if 'recipe_name' in json else None
        self.recipe_method = json["recipe_method"] if 'recipe_method' in json else None
        self.recipe_srm = json["recipe_srm"] if 'recipe_srm' in json else None
        self.recipe_batch_size = json["recipe_batch_size"] if 'recipe_batch_size' in json else None
        self.recipe_rating = json["recipe_rating"] if 'recipe_rating' in json else None
        self.recipe_description = json["recipe_description"] if 'recipe_description' in json else None
        self.style_id = json["style_id"] if 'style_id' in json else None
        self.image_id = json["image_id"] if 'image_id' in json else None
        self.notes_id = json["notes_id"] if 'notes_id' in json else None
        self.malts = populate_malts(json['ingredient_malts']) if 'ingredient_malts' in json else list()
        self.yeasts = populate_yeasts(json['ingredient_yeasts']) if 'ingredient_yeasts' in json else list()
        self.hops = populate_hops(json['ingredient_hops']) if 'ingredient_hops' in json else list()
        self.others = populate_others(json['ingredient_others']) if 'ingredient_others' in json else list()
    
class malt:
    
    def __init__(self, malt_id, malt_ingred_qty, malt_ingred_time, malt_ingred_type, malt_ingred_temp, malt_ingred_stage):
        self.malt_id = malt_id
        self.malt_ingred_qty = malt_ingred_qty
        self.malt_ingred_time = malt_ingred_time
        self.malt_ingred_type = malt_ingred_type
        self.malt_ingred_temp = malt_ingred_temp
        self.malt_ingred_stage = malt_ingred_stage
        
class yeast:
    
    def __init__(self, yeast_id, yeast_ingred_qty, yeast_ingred_starter, yeast_ingred_time):
        self.yeast_id = yeast_id
        self.yeast_ingred_qty = yeast_ingred_qty
        self.yeast_ingred_starter = yeast_ingred_starter
        self.yeast_ingred_time = yeast_ingred_time
        
class hops:
    
    def __init__(self, hops_id, hops_ingred_qty, hops_ingred_time, hops_ingred_use):
        self.hops_id = hops_id
        self.hops_ingred_qty = hops_ingred_qty
        self.hops_ingred_time = hops_ingred_time
        self.hops_ingred_use = hops_ingred_use
        
class other:
    
    def __init__(self, other_id, other_ingred_qty, other_ingred_time):  
        self.other_id = other_id
        self.other_ingred_qty = other_ingred_qty
        self.other_ingred_time = other_ingred_time
        
def populate_malts(json_malts):
    malts = list()
    for m in json_malts:
        malt_id = m["malt_id"]
        malt_ingred_qty = m["malt_ingred_qty"]
        malt_ingred_time = m["malt_ingred_time"] if 'malt_ingred_time' in m else None 
        malt_ingred_type = m["malt_ingred_type"] if 'malt_ingred_type' in m else None
        malt_ingred_temp = m["malt_ingred_temp"] if 'malt_ingred_temp' in m else None
        malt_ingred_stage = m["malt_ingred_stage"] if 'malt_ingred_stage' in m else None
        malts.Add(malt_id, malt_ingred_qty, malt_ingred_time, malt_ingred_type, malt_ingred_temp, malt_ingred_stage)
    return malts

def populate_yeasts(json_yeasts):
    yeasts = list()
    for y in json_yeasts:
        yeast_id = y["yeast_id"]
        yeast_ingred_qty = y["yeast_ingred_qty"]
        yeast_ingred_starter = y["yeast_ingred_starter"] if 'yeast_ingred_starter' in y else None 
        yeast_ingred_time = y["yeast_ingred_time"] if 'yeast_ingred_time' in y else None 
        yeasts.Add(yeast_id, yeast_ingred_qty, yeast_ingred_starter, yeast_ingred_time)
    return yeasts

def populate_hops(json_hops):
    hops = list()
    for h in json_hops:
        hops_id = h['hops_id']
        hops_ingred_qty = h['hops_ingred_qty']
        hops_ingred_time = h['hops_ingred_time'] if 'hops_ingred_time' in h else None 
        hops_ingred_use = h['hops_ingred_use'] if 'hops_ingred_use' in h else None 
        hops.Add(hops_id, hops_ingred_qty, hops_ingred_time, hops_ingred_use)
    return hops

def populate_others(json_others):
    others = list()
    for o in json_others:
        other_id = o['other_id']
        other_ingred_qty = o['other_ingred_qty']
        other_ingred_time = o['other_ingred_time'] if 'other_ingred_time' in o else None 
        others.Add(other_id, other_ingred_qty, other_ingred_time)
    return others