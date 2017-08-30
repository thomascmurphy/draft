from .models import *

class Card():
    #methods
    @classmethod
    def get_cards(params):
        cards = select_items('cards', params)
        return cards

    @classmethod
    def get_card_by_id(id):
        card = select_items('cards', "id='%i'" % id)[0]
        return card

    @classmethod
    def create_card(params):
        card = insert_item('cards', params)
        return card

    @classmethod
    def delete_card(id):
        card = delete_item_with_id('cards', "id='%i'" % id)
        return true
