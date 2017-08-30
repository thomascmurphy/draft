from .models import *

class Player():
    #methods
    @classmethod
    def get_players(params):
        players = select_items('players', params)
        return players

    @classmethod
    def get_player_by_hash(hash):
        player = select_items('players', "hash='%s'" % hash)[0]
        return player

    @classmethod
    def create_player(params):
        player = insert_item('players', params)
        return player

    @classmethod
    def delete_player(id):
        player = delete_item_with_id('players', "id='%i'" % id)
        return true
