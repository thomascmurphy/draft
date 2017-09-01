from mtgsdk import Set, Card

from .models import *
from .pack_card import PackCard
import pdb

class Pack():
    #methods
    @staticmethod
    def get_packs(params):
        packs = select_items('packs', params)
        return packs

    @staticmethod
    def get_pack_by_id(id):
        pack = select_items('packs', "id='%i'" % id)[0]
        return pack

    @staticmethod
    def create_pack(set_code, player_id, number):
        pack = insert_item('packs', {'set_code': set_code, 'player_id': player_id, 'number': number})
        cards = Set.generate_booster(set_code)
        card_ids_used = []
        for card in cards:
            while card.multiverse_id in card_ids_used:
                card = Card.where(set=set_code).where(rarity=card.rarity).all()[0]
            card_ids_used.append(card.id)
            PackCard.create_pack_card(card.multiverse_id, pack['id'])
        return pack

    @staticmethod
    def delete_pack(id):
        pack = delete_item_with_id('packs', "id='%i'" % id)
        return true
