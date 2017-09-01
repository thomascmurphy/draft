from .models import *
from .card import Card

class PackCard():
    #methods
    @staticmethod
    def get_pack_cards(params):
        pack_cards = select_items('pack_cards', params)
        return pack_cards

    @staticmethod
    def get_pack_card_by_id(id):
        pack_card = select_items('pack_cards', "id='%i'" % id)[0]
        return pack_card

    @staticmethod
    def create_pack_card(card_id, pack_id, deck_id=None, pick=None, sideboard=None):
        pack_card = insert_item('pack_cards', {'card_id': card_id, 'pack_id': pack_id, 'deck_id': deck_id, 'pick': pick, 'sideboard': sideboard})
        return pack_card

    @staticmethod
    def update_pack_cards(values, params):
        pack_card = update_item('pack_cards', values, params)
        return pack_card

    @staticmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true
