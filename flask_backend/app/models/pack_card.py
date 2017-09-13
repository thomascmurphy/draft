from .models import *
from .card import Card
from .pack import Pack

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
    def create_pack_card(card_id, pack_id, deck_id=None, pick=None, sideboard=None):
        pack_card = insert_item('pack_cards', {'card_id': card_id, 'pack_id': pack_id, 'deck_id': deck_id, 'pick': pick, 'sideboard': sideboard})
        return pack_card

    @staticmethod
    def update_pack_cards(values, params):
        pack_card = update_item('pack_cards', values, params)
        return pack_card

    @staticmethod
    def get_pick_number(pack_id):
        pack_cards = Pack.get_all_cards(pack_id)
        last_pick = max([pack_card["pick"] for pack_card in pack_cards])
        current_pick = last_pick + 1
        return current_pick

    @staticmethod
    def update_pack_card_by_id(id, values):
        return update_pack_cards(values, ["id=%i", id])

    @staticmethod
    def pick_pack_card(pack_card_id, deck_id, next_player_id):
        pick_number = get_pick_number(pack_card_id)
        pack_card = update_pack_card_by_id(pack_card_id, {pick_number: pick_number, deck_id: deck_id})
        pack = Pack.update_pack_by_id(pack_card['pack_id'], {player_id: next_player_id})
        return pack_card

    @staticmethod
    def add_card_images_to_pack_cards(pack_cards):
        card_ids = [pack_card['id'] for pack_card in pack_cards]
        cards = select_items('cards', ["cards.id in (%s)" % ",".join(list(map(str, card_ids)))])
        card_images = {card['id']: card['image_url'] for card in cards}
        pack_cards = [dict({'image_url': card_images[pack_card['card_id']]}, **pack_card) for pack_card in pack_cards]
        return pack_cards

    @staticmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true
