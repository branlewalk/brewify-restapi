import json
from flask import Flask, jsonify, render_template

# Connection String 'mysql+pymysql://db/brew_project'
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False

@app.route('/')
def index():
    pass

@app.route('/recipes')
def recipes():
    pass

@app.route('/session')
def session():
    pass

@app.route('/ingredients')
def ingredients():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')