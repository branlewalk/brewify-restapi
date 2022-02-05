import json
from flask import Flask, jsonify, render_template
import pymysql

db = pymysql.connect(user='root', passwd='password', host='localhost', database='brewify_db')
cursor = db.cursor()

# Connection String 'mysql+pymysql://db/brew_project'
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False

@app.route('/')
def index():
    pass

@app.route('/recipes', methods=['POST'])
def recipes():
    sproc = "CreateRecipe"
    params = ('HelloWorldRecipe', 'All-Grain', 10, 5.0, 2, 'First Recipe', 1, 1, None)
    call_stored_procedure(sproc, params)
    

@app.route('/session')
def session():
    pass

@app.route('/ingredients')
def ingredients():
    pass

def call_stored_procedure(sproc, params):
    cursor.callproc(sproc, params) 
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    app.run(debug=True, port=7099, host='0.0.0.0')