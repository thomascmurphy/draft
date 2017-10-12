from .models import *

class Card():
    #methods
    @staticmethod
    def get_cards(params, order=[]):
        cards = select_items('cards', params, order)
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
    def create_card(name, multiverse_id, cmc, colors, set_code, mana_cost, types, rarity, number):
        card = insert_item('cards', {'name': name, 'multiverse_id': multiverse_id, 'cmc': cmc, 'colors': colors, 'set_code': set_code, 'mana_cost': mana_cost, 'types': types, 'rarity': rarity, 'number': number})
        return card

    @staticmethod
    def delete_card(id):
        card = delete_item_with_id('cards', "id='%i'" % id)
        return true

    @staticmethod
    def calculate_rating(card, deck_cards_color_count, deck_cards_cmc_count):
        base_rating = card['rating'] if card['rating'] else 0
        cmc = card['cmc']
        cmc_size = deck_cards_cmc_count[str(cmc)] if str(cmc) in deck_cards_cmc_count else 0
        symbols = re.findall(r'\{.+\}', card['mana_cost'])
        colors = card['colors']
        deck_card_count = sum(deck_cards_cmc_count.values())
        cast_rating = 20 / (len(colors) + len(symbols) + cmc + 1)
        color_rating = 0
        for color in colors:
            color_rating += (50 * deck_cards_color_count[color.lower()] / (deck_card_count + 10) )
        color_rating = color_rating / len(colors) if colors else 5
        curve_rating = ((deck_card_count + 1) / (cmc_size + 1)) / ((cmc - 2)**2 + 1)
        return {'overall_rating': base_rating + cast_rating + color_rating + curve_rating, 'base_rating': base_rating, 'cast_rating': cast_rating, 'color_rating': color_rating, 'curve_rating': curve_rating}
