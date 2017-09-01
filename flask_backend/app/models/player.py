import base64
from flask import current_app

from .models import *
from .deck import Deck

class Player():
    #methods
    @staticmethod
    def get_players(params):
        players = select_items('players', params)
        return players

    @staticmethod
    def get_player_by_hash(hash):
        #cipher = AES.new(current_app.config['PLAYER_HASH_KEY'])
        #hash = base64.encodestring(cipher.encrypt("%016d"%id))
        #id = int(cipher.decrypt(base64.decodestring(hash)))
        player = select_items('players', "id='%i'" % id)[0]
        return player

    @staticmethod
    def create_player(email, pod_id):
        player = insert_item('players', {'email': email, 'pod_id': pod_id})
        deck = Deck.create_deck(player['id'])
        return player

    @staticmethod
    def delete_player(id):
        player = delete_item_with_id('players', "id='%i'" % id)
        return true

    @staticmethod
    def get_player_pack(player_id):
        packs = select_items('packs', ["player_id = %i" % player_id, "complete = false"], ['number ASC'])
        return packs[0]
