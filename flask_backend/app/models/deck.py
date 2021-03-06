import collections
from .models import *
from .pack_card import PackCard

class Deck():
    #methods
    @staticmethod
    def get_decks(params):
        decks = select_items('decks', params)
        return decks

    @staticmethod
    def get_deck_by_id(id):
        deck = select_item_by_id('decks', id)
        return deck

    @staticmethod
    def get_deck_by_player_id(player_id):
        deck = select_first_item('decks', ["player_id=%i" % player_id])
        return deck

    @staticmethod
    def create_deck(player_id):
        deck = insert_item('decks', {'player_id': player_id})
        return deck

    @staticmethod
    def delete_deck(id):
        deck = delete_item_with_id('decks', id)
        return true

    @staticmethod
    def get_cards(deck_id):
        deck = select_item_by_id('decks', deck_id)
        deck_cards = select_items('pack_cards', ["deck_id=%i" % deck_id], ["pack_cards.pick_number ASC"])
        return PackCard.add_card_data_to_pack_cards(deck_cards)

    @staticmethod
    def get_stats(deck_id, deck_cards=[]):
        if deck_cards == []:
          deck_cards = Deck.get_cards(deck_id)
        deck_cards_color_count = {'white': 0, 'blue': 0, 'black': 0, 'red': 0, 'green': 0}
        deck_cards_cmc_count = collections.defaultdict(int)
        for deck_card in deck_cards:
            deck_cards_color_count['white'] += len(re.findall(r'W', deck_card['mana_cost']))
            deck_cards_color_count['blue'] += len(re.findall(r'U', deck_card['mana_cost']))
            deck_cards_color_count['black'] += len(re.findall(r'B', deck_card['mana_cost']))
            deck_cards_color_count['red'] += len(re.findall(r'R', deck_card['mana_cost']))
            deck_cards_color_count['green'] += len(re.findall(r'G', deck_card['mana_cost']))
            deck_cards_cmc_count[str(deck_card['cmc'])] += 1
        return {'deck_cards_color_count': deck_cards_color_count, 'deck_cards_cmc_count': deck_cards_cmc_count, 'deck_cards_count': len(deck_cards)}
