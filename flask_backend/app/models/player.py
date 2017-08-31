from Crypto.Cipher import AES
import base64
from flask import current_app

from .models import *

class Player():
    #methods
    @classmethod
    def get_players(params):
        players = select_items('players', params)
        return players

    @classmethod
    def get_player_by_hash(hash):
        cipher = AES.new(current_app.config['PLAYER_HASH_KEY'])
        #hash = base64.encodestring(cipher.encrypt("%016d"%id))
        id = int(cipher.decrypt(base64.decodestring(hash)))
        player = select_items('players', "id='%i'" % id)[0]
        return player

    @classmethod
    def create_player(email, pod_id):
        player = insert_item('players', {'email': email, 'pod_id': pod_id})
        deck = Deck.create_deck(player.id)
        return player

    @classmethod
    def delete_player(id):
        player = delete_item_with_id('players', "id='%i'" % id)
        return true
