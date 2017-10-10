"""
 Simple API endpoint for returning sets
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
#from mtgsdk import Set
from ..models import Set

sets = Blueprint('sets', __name__, url_prefix='/api/v1/sets')

# @sets.route('/', methods=['GET'])
# def get_sets():
#     sets = Set.all()
#     set_list = list(map(lambda set: {'name': set.name, 'code': set.code, 'release_date': set.release_date}, sets))
#     result_json = sorted(set_list, key=lambda set: set['release_date'], reverse=True)
#     return jsonify({'sets': result_json}), 201

@sets.route('/', methods=['GET'])
def get_sets():
  sets = Set.get_sets([])
  result_json = sorted(sets, key=lambda set: set['release_date'], reverse=True)
  return jsonify({'sets': result_json}), 201

@sets.route('/seed', methods=['GET'])
def seed_sets():
  sets = Set.seed_data()
  return jsonify({'sets': sets}), 201

@sets.route('/<set_code>/booster', methods=['GET'])
def booster(set_code):
  cards = Set.generate_booster(set_code)
  return jsonify({'cards': cards}), 201
