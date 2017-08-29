"""
 Simple API endpoint for returning players
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)

players = Blueprint('players', __name__, url_prefix='/api/v1/players')

@players.route('/<player_hash>', methods=['GET'])
def get_player(player_hash):
    players = select_items('players', ("hash=%s" % player_hash))
    return jsonify(players), 201

@players.route('/<player_hash>/deck', methods=['GET'])
def get_player_deck(player_hash):
    players = select_items('players', ("hash=%s" % player_hash))
    return jsonify(players), 201

@players.route('/<player_hash>/pack', methods=['GET'])
def get_player_pack(player_hash):
    players = select_items('players', ("hash=%s" % player_hash))
    return jsonify(players), 201
