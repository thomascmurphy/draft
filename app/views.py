#!flask/bin/python
import app import app
from flask import Flask, jsonify, json, abort, request, make_response, url_for, render_template

from mtgsdk import Set
from mtgsdk import Card

import pdb

from models import *


@app.route('/')
def index():
    return render_template('index.html')

#====SETS
@app.route('/api/v1/sets', methods=['GET'])
def api_get_sets():
    sets = select_items('sets', ())
    return jsonify(sets), 201

#====PODS
@app.route('/api/v1/pods', methods=['GET'])
def api_get_pods():
    return render_template('index.html')

@app.route('/api/v1/pods', methods=['POST'])
def api_post_pods():
    return render_template('index.html')

@app.route('/api/v1/pods', methods=['DELETE'])
def api_delete_pods():
    return render_template('index.html')

#====PLAYERS
@app.route('/api/v1/players', methods=['GET'])
def api_get_players():
    return render_template('index.html')

@app.route('/api/v1/players', methods=['POST'])
def api_post_players():
    return render_template('index.html')

@app.route('/api/v1/players', methods=['DELETE'])
def api_delete_players():
    return render_template('index.html')

#====PACKS
@app.route('/api/v1/packs', methods=['GET'])
def api_get_packs():
    return render_template('index.html')

@app.route('/api/v1/packs', methods=['POST'])
def api_post_packs():
    return render_template('index.html')

@app.route('/api/v1/packs', methods=['DELETE'])
def api_delete_packs():
    return render_template('index.html')

#====DECKS
@app.route('/api/v1/decks', methods=['GET'])
def api_get_decks():
    return render_template('index.html')

@app.route('/api/v1/decks', methods=['POST'])
def api_post_decks():
    return render_template('index.html')

@app.route('/api/v1/decks', methods=['DELETE'])
def api_delete_decks():
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
