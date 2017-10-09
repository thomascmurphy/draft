from .models import *

class Card():
    #methods
    @staticmethod
    def get_cards(params):
        cards = select_items('cards', params)
        return cards

    @staticmethod
    def get_card_by_id(id):
        card = select_item_by_id('cards', id)
        return card

    @staticmethod
    def get_random_card(params):
        card = select_first_item('cards', params, ["RANDOM()"])
        return card

    @staticmethod
    def create_card(name, multiverse_id, cmc, color_identity, set_code, mana_cost, types, rarity, number):
        card = insert_item('cards', {'name': name, 'multiverse_id': multiverse_id, 'cmc': cmc, 'color_identity': color_identity, 'set_code': set_code, 'mana_cost': mana_cost, 'types': types, 'rarity': rarity, 'number': number})
        return card

    @staticmethod
    def delete_card(id):
        card = delete_item_with_id('cards', "id='%i'" % id)
        return true
