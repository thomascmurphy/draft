"""
 Simple API endpoint for returning players
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from ..models import Player

players = Blueprint('players', __name__, url_prefix='/api/v1/players')

@players.route('/<player_hash>', methods=['GET'])
def get_player(player_hash):
    player = Player.get_player_by_hash(player_hash)
    return jsonify(players), 201

@players.route('/<player_hash>/deck', methods=['GET'])
def get_player_deck(player_hash):
    player = Player.get_player_by_hash(player_hash)
    deck = Deck.get_decks(["player_id=%i" % player_id])
    return jsonify(players), 201

@players.route('/<player_hash>/pack', methods=['GET'])
def get_player_pack(player_hash):
    player = Player.get_player_by_hash(player_hash)
    return jsonify(players), 201
