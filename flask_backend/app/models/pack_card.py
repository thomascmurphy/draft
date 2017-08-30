from .models import *

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
    def create_pack_card(params):
        pack_card = insert_item('pack_cards', params)
        return pack_card

    @classmethod
    def update_pack_card(values, params):
        pack_card = update_item('pack_cards', values, params)
        return pack_card

    @classmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true
