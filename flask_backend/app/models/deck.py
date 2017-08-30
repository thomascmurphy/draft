from .models import *

class Deck():
    #methods
    @classmethod
    def get_decks(params):
        decks = select_items('decks', params)
        return decks

    @classmethod
    def get_deck_by_id(id):
        deck = select_items('decks', "id='%i'" % id)[0]
        return deck

    @classmethod
    def create_deck(player_id):
        deck = insert_item('decks', {'player_id': player_id})
        return deck

    @classmethod
    def delete_deck(id):
        deck = delete_item_with_id('decks', "id='%i'" % id)
        return true
