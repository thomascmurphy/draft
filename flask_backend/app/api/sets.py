"""
 Simple API endpoint for returning sets
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from ..models import Set, PackCard
from ..models.models import *

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
  reseed = request.args.get('reseed')
  sets = Set.seed_data(reseed)
  return jsonify({'sets': sets}), 201

@sets.route('/<set_code>/booster', methods=['GET'])
def booster(set_code):
  cards = Set.generate_booster(set_code)
  return jsonify({'cards': cards}), 201
#
# @sets.route('/transfer_pack_cards')
# def transfer_pack_cards():
#   old_pack_cards = select_items('pack_cards_temp', [])
#   for old_pack_card in old_pack_cards:
#     old_card = select_first_item('cards_temp', ["id='%s'" % old_pack_card['card_id']])
#     new_card = select_first_item('cards', ["multiverse_id=%i" % int(old_card['multiverse_id'])])
#     updates = ["card_id=%i" % new_card['id'], "deck_id=%i" % int(old_pack_card['deck_id'])] if old_pack_card['deck_id'] else ["card_id=%i" % new_card['id']]
#     new_pack_card = PackCard.update_pack_card_by_id(int(old_pack_card['id']), updates)
#   return jsonify({'cards': cards}), 201

@sets.route('/transfer_ratings', methods=['GET'])
def transfer_ratings():
  card_ratings = select_items('card_ratings', [])
  cards = select_items('cards', [])
  for card in cards:
    ratings = [float(card_rating['rating']) for card_rating in card_ratings if card_rating['name'] == card['name'] and card_rating['set_code'] == card['set_code']]
    if ratings and ratings[0]:
      card_update = update_item('cards', ["rating=%i" % int(ratings[0] * 10)], ["id=%i" % card['id']])
  return jsonify({'cards': cards}), 201