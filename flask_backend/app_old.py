#!flask/bin/python
import os
import sqlite3
from flask import Flask, jsonify, json, abort, request, make_response, url_for, render_template

from mtgsdk import Set
from mtgsdk import Card

import pdb

app = Flask(__name__)
# app.config.from_object(__name__)
#
# # Load default config and override config from an environment variable
# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, 'draft.db'),
#     SECRET_KEY='development key',
#     USERNAME='admin',
#     PASSWORD='default'
# ))
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#
# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booster', methods=['GET'])
def display_booster():
    the_set = request.args.get('set', "LEA")
    booster = Set.generate_booster(the_set)
    booster_json = list(map(lambda card: {'name': card.name, 'imageUrl': card.image_url}, booster))
    return render_template('booster.html', booster=booster)

@app.route('/api/v1/booster', methods=['GET'])
def api_get_booster():
    the_set = request.args.get('set', "LEA")
    booster = Set.generate_booster(the_set)
    #pdb.set_trace()
    booster_json = list(map(lambda card: {'name': card.name, 'imageUrl': card.image_url}, booster))
    return jsonify(booster_json), 201






if __name__ == '__main__':
    app.run(debug=True)
