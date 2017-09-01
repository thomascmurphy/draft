from __future__ import print_function # In python 2.7
from mtgsdk import Card as CardSDK

from .models import *
from .card import Card
import pdb
import sys

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
    def create_pack_card(card_multiverse_id, pack_id, deck_id=None, pick=None, sideboard=None):
        cards = select_items('cards', ["multiverse_id=%i" % card_multiverse_id])
        if cards:
          card = cards[0]
        else:
          card_data = CardSDK.find(card_multiverse_id)
          print('SDK Call', file=sys.stderr)
          card = Card.create_card(card_data.name, card_data.image_url, card_data.multiverse_id, card_data.cmc, str(card_data.color_identity), card_data.set)
        try:
          pack_card = insert_item('pack_cards', {'card_id': card['id'], 'pack_id': pack_id, 'deck_id': deck_id, 'pick': pick, 'sideboard': sideboard})
        except:
          pdb.set_trace()
        return pack_card

    @staticmethod
    def update_pack_cards(values, params):
        pack_card = update_item('pack_cards', values, params)
        return pack_card

    @staticmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true
