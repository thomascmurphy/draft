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
    def create_card(name, image_url, multiverse_id, cmc, color_identity, set_code):
        card = insert_item('cards', {'name': name, 'image_url': image_url, 'multiverse_id': multiverse_id, 'cmc': cmc, 'color_identity': color_identity, 'set_code': set_code})
        return card

    @classmethod
    def delete_card(id):
        card = delete_item_with_id('cards', "id='%i'" % id)
        return true
