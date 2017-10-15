"""
 Simple API endpoint for returning players
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from ..models import Player, Pack, Deck, Pod, PackCard, Card
import pdb
import sys

players = Blueprint('players', __name__, url_prefix='/api/v1/players')

# @players.route('/<player_hash>', methods=['GET'])
# def get_player(player_hash):
#     player = Player.get_player_by_hash(player_hash)
#     return jsonify({'player': player}), 201

test_1_pack_card_ids = [435176, 435197, 435366, 435282, 435299, 435249, 435159, 435341, 435228, 435356, 435178, 435188, 435302, 435330, 435277, 435433]
test_1_deck_card_ids = [435387, 435274, 435292, 435245, 435163, 435219, 435364, 435350, 435190, 435277, 435193, 435278, 435195, 435281, 435199, 435429]

test_2_pack_card_ids = [435378, 435384, 435353, 435277, 435249]
test_2_deck_card_ids = []

@players.route('', methods=['GET'])
def get_players():
    email = request.args.get('email')
    query = []
    if email:
      query = ["email = '%s'" % email.lower()]
      players = Player.get_players(query)
      pod_hashes = {player['pod_id']: {'id': player['id'], 'hash': player['hash'], 'is_owner': player['is_owner']} for player in players}
      pods = Pod.get_pods(["pods.id in (%s)" % ",".join(list(map(str, pod_hashes.keys())))])
      pods = [dict({'player_id': pod_hashes[pod['id']]['id'], 'player_hash': pod_hashes[pod['id']]['hash'], 'is_owner':pod_hashes[pod['id']]['is_owner']}, **pod) for pod in pods]
    else:
      players = []
      pods = []
    return jsonify({'players': players, 'pods': pods}), 201

@players.route('/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.get_player_by_id(player_id)
    pod = Pod.get_pod_by_id(player['pod_id'])
    return jsonify({'player': player, 'pod': pod}), 201

@players.route('/<player_hash>/deck', methods=['GET'])
def get_player_deck_by_hash(player_hash):
    if player_hash in ['test1', 'test2']:
        if player_hash == 'test1':
            deck_multiverse_ids = test_1_deck_card_ids
        elif player_hash == 'test2':
            deck_multiverse_ids = test_2_deck_card_ids
        deck_multiverse_orders = ["multiverse_id=%i DESC" % multiverse_id for multiverse_id in deck_multiverse_ids]
        cards = Card.get_cards(["multiverse_id in (%s)" % ",".join(list(map(str, deck_multiverse_ids)))], deck_multiverse_orders)
        deck_cards = [dict({'deck_id': 0, 'pack_id': 0, 'pick_number': index + 1, 'image_url': "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%i&type=card" % card['multiverse_id'], 'card_id': card['id']}, **card) for index, card in enumerate(cards)]
        deck = {}
        player = {'hash': player_hash, 'name': player_hash, 'id': 0, 'pod_id': 0}
    else:
      player = Player.get_player_by_hash(player_hash)
      deck = Player.get_player_deck(player['id'])
      deck_cards = Deck.get_cards(deck['id'])
    return jsonify({'player': player, 'deck': deck, 'deck_cards': deck_cards}), 201

# @players.route('/<int:player_id>/deck', methods=['GET'])
# def get_player_deck_by_id(player_id):
#     player = Player.get_player_by_id(player_id)
#     deck = Player.get_player_deck(player['id'])
#     cards = Deck.get_cards(deck['id'])
#     return jsonify({'player': player, 'deck': deck, 'cards': cards}), 201

@players.route('/<player_hash>/pack', methods=['GET'])
def get_player_pack_by_hash(player_hash):
    if player_hash in ['test1', 'test2']:
        if player_hash == 'test1':
            card_multiverse_ids = test_1_pack_card_ids
            deck_multiverse_ids = test_1_deck_card_ids
        elif player_hash == 'test2':
            card_multiverse_ids = test_2_pack_card_ids
            deck_multiverse_ids = test_2_deck_card_ids
        card_multiverse_orders = ["multiverse_id=%i DESC" % multiverse_id for multiverse_id in card_multiverse_ids]
        cards = Card.get_cards(["multiverse_id in (%s)" %  ",".join(list(map(str, card_multiverse_ids)))], card_multiverse_orders)
        cards_deck = Card.get_cards(["multiverse_id in (%s)" %  ",".join(list(map(str, deck_multiverse_ids)))])
        deck_cards = [dict({'deck_id': 0, 'pack_id': 0, 'pick_id': index + 1, 'card_id': card['id']}, **card) for index, card in enumerate(cards_deck)]
        deck_stats = Deck.get_stats(0, deck_cards)
        pack_cards = [dict({'deck_id': None, 'pack_id': 0, 'pick_id': None, 'image_url': "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%i&type=card" % card['multiverse_id'], 'card_id': card['id']}, **card) for card in cards]
        player = {'hash': player_hash, 'name': player_hash, 'id': 0, 'pod_id': 0}
        pack = {'id': 0, 'player_id': 0, 'number': 1}
        pod = {'id': 0, 'name': player_hash}
    else:
        player = Player.get_player_by_hash(player_hash)
        pack = Player.get_player_pack(player['id'])
        pack_cards = Pack.get_all_cards(pack['id']) if pack else []
        pod = Pod.get_pod_by_id(player['pod_id'])
        deck = Player.get_player_deck(player['id'])
        deck_stats = Deck.get_stats(deck['id'])
    pack_cards = PackCard.add_ratings(pack_cards, deck_stats['deck_cards_color_count'], deck_stats['deck_cards_cmc_count'])
    return jsonify({'player': player, 'pack': pack, 'pack_cards': pack_cards, 'pod': pod}), 201

# @players.route('/<int:player_id>/pack', methods=['GET'])
# def get_player_pack_by_id(player_id):
#     player = Player.get_player_by_id(player_id)
#     pack = Player.get_player_pack(player_id)
#     cards = Pack.get_available_cards(pack['id'])
#     return jsonify({'player': player, 'pack': pack, 'cards': cards}), 201

@players.route('/pick', methods=['POST'])
def create_pick():
    pack_card_id = int(request.json['pack_card_id'])
    player_id = int(request.json['player_id'])
    pack_card = PackCard.get_pack_card_by_id(pack_card_id)
    pack = Pack.get_pack_by_id(pack_card['pack_id'])
    player = Player.get_player_by_id(player_id)
    pod = Pod.get_pod_by_id(player['pod_id'])
    player_ids = pod['player_ids']
    next_player_id = player_ids[(player_ids.index(player['id']) + 1)%len(player_ids)]
    next_player = Player.get_player_by_id(next_player_id)
    deck = Deck.get_deck_by_player_id(player['id'])
    #pick_number = Pack.get_pick_number(Pack.get_all_cards(pack['id']))
    deck_cards = Deck.get_cards(deck['id'])
    pick_number = len(deck_cards) + 1
    pack_card = Player.pick_pack_card(pack_card_id, deck['id'], player_id, next_player, pick_number, pack['player_id'], pod['id'])

    pack = Player.get_player_pack(player['id'])
    pack_cards = Pack.get_all_cards(pack['id']) if pack else []
    deck_cards = Deck.get_cards(deck['id']) if deck else []
    pod = Pod.get_pod_by_id(player['pod_id'])
    return jsonify({'player': player, 'pack': pack, 'pack_cards': pack_cards, 'deck_cards': deck_cards, 'pod': pod}), 201

@players.route('/update_deck_card', methods=['PUT'])
def update_deck_card():
    deck_card_json = request.json['deck_card']
    id = deck_card_json['id']
    deck_id = deck_card_json['deck_id']
    sideboard = deck_card_json['sideboard']
    if deck_id > 0 and sideboard > -1:
        deck_card = PackCard.update_pack_card_by_id(id, ["sideboard=%i" % sideboard])
        deck_card_with_data = PackCard.add_card_data_to_pack_cards([deck_card])[0]
    return jsonify({'deck_card': deck_card_with_data}), 201

@players.route('/<player_hash>/card_images', methods=['GET'])
def get_player_card_images_by_hash(player_hash):
    if player_hash in ['test1', 'test2']:
      card_image_urls = []
    else:
      player = Player.get_player_by_hash(player_hash)
      pod_id = player['pod_id']
      pod_players = Player.get_players(['pod_id=%i' % pod_id])
      pod_player_ids = [player['id'] for player in pod_players]
      pod_packs = Pack.get_packs(['packs.player_id IN (%s)' % ",".join(list(map(str, pod_player_ids)))])
      pod_pack_ids = [pack['id'] for pack in pod_packs]
      pod_pack_cards = PackCard.get_pack_cards(['pack_cards.pack_id IN (%s)' % ",".join(list(map(str, pod_pack_ids)))])
      pod_pack_cards_with_images = PackCard.add_card_data_to_pack_cards(pod_pack_cards)
      card_image_urls = [card['image_url'] for card in pod_pack_cards_with_images]
    return jsonify({'card_image_urls': card_image_urls}), 201
