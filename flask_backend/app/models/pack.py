from mtgsdk import Set, Card

from .models import *
from .pack_card import PackCard

class Pack():
    #methods
    @classmethod
    def get_packs(params):
        packs = select_items('packs', params)
        return packs

    @classmethod
    def get_pack_by_id(id):
        pack = select_items('packs', "id='%i'" % id)[0]
        return pack

    @classmethod
    def create_pack(set_code, player_id, order):
        pack = insert_item('packs', {'set_code': set_code, 'player_id': player_id, 'order': order})
        cards = Set.generate_booster(set_code)
        card_ids_used = []
        for card in cards:
            while card['id'] in card_ids_used:
                card = Card.where(set=set_code).where(rarity=card['rarity'])
            PackCard.create_pack_card(card['card_multiverse_id'], card['pack_id'])
        return pack

    @classmethod
    def delete_pack(id):
        pack = delete_item_with_id('packs', "id='%i'" % id)
        return true
