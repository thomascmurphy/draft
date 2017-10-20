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
        pack_card = select_item_by_id('pack_cards', id)
        return pack_card

    @staticmethod
    def create_pack_card(card_id, pack_id, deck_id=None, pick_number=None, sideboard=None):
        pack_card = insert_item('pack_cards', {'card_id': card_id, 'pack_id': pack_id, 'deck_id': deck_id, 'pick_number': pick_number, 'sideboard': sideboard})
        return pack_card

    @staticmethod
    def update_pack_card(values, params):
        pack_cards_update = update_item('pack_cards', values, params)
        pack_card = select_first_item('pack_cards', params)
        return pack_card

    @staticmethod
    def update_pack_card_by_id(id, values):
        return PackCard.update_pack_card(values, ["pack_cards.id=%i" % id])

    @staticmethod
    def add_card_data_to_pack_cards(pack_cards):
        card_ids = [pack_card['card_id'] for pack_card in pack_cards]
        cards = select_items('cards', ["cards.id in (%s)" % ",".join(list(map(str, card_ids)))])
        card_data = {card['id']: {'image_url': "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%i&type=card" % card['multiverse_id'], 'cmc': card['cmc'], 'colors': card['colors'], 'mana_cost': card['mana_cost'], 'types': card['types'], 'rating': card['rating'], 'name': card['name']} for card in cards}
        pack_cards = [dict(card_data[pack_card['card_id']], **pack_card) for pack_card in pack_cards]
        return pack_cards

    @staticmethod
    def add_ratings(pack_cards, deck_cards_color_count, deck_cards_cmc_count):
        return add_ratings_to_pack_cards(pack_cards, deck_cards_color_count, deck_cards_cmc_count)

    @staticmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true
