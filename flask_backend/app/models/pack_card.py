from mtgsdk import Card as CardSDK

from .models import *
from .card import Card as DBCard

class PackCard():
    #methods
    @classmethod
    def get_pack_cards(params):
        pack_cards = select_items('pack_cards', params)
        return pack_cards

    @classmethod
    def get_pack_card_by_id(id):
        pack_card = select_items('pack_cards', "id='%i'" % id)[0]
        return pack_card

    @classmethod
    def create_pack_card(card_multiverse_id, pack_id, deck_id=null, pick=null, sideboard=false):
        card = select_items('card', "multiverse_id=%i" % card_multiverse_id)
        if not card:
            card_data = CardSDK.find(card_multiverse_id)
            card = Card.create_card(card_data['name'], card_data['image_url'], card_data['multiverse_id'], card_data['cmc'],card_data['color_identity'], card_data['set_code'])
        pack_card = insert_item('pack_cards', {'card_id': card.id, 'pack_id': pack_id, 'deck_id': deck_id, 'pick': pick, 'sideboard': sideboard})
        return pack_card

    @classmethod
    def update_pack_cards(values, params):
        pack_card = update_item('pack_cards', values, params)
        return pack_card

    @classmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true
