#!flask/bin/python
from flask import Flask, jsonify, json, abort, request, make_response, url_for

from mtgsdk import Set
from mtgsdk import Card

import pdb

app = Flask(__name__)

@app.route('/api/v1/booster', methods=['GET'])
def get_booster():
    the_set = request.args.get('set', "LEA")
    booster = Set.generate_booster(the_set)
    #pdb.set_trace()
    booster_json = list(map(lambda card: {'name': card.name, 'imageUrl': card.image_url}, booster))
    return jsonify(booster_json), 201

if __name__ == '__main__':
    app.run(debug=True)
