from .models import *
from .card import Card

class Set():
    #methods
    @staticmethod
    def get_sets(params):
        sets = select_items('sets', params)
        return sets

    @staticmethod
    def get_set_by_id(id):
        set = select_item_by_id('sets', id)
        return set

    @staticmethod
    def get_set_by_code(code):
        set = select_first_item('sets', ["sets.code=%s" % code])
        return set

    @staticmethod
    def create_set(name, code, booster, release_date, card_count):
        set = insert_item('sets', {'name': name, 'code': code, 'booster': booster, 'release_date': release_date, 'card_count': card_count})
        return set

    @staticmethod
    def delete_set(id):
        set = delete_item_with_id('sets', "id='%i'" % id)
        return true

    @staticmethod
    def booster_rarities(booster):
        clean_booster = []
        for rarity in booster:
            if isinstance(rarity, list):
                if rarity[0] == "rare" and rarity[1] == "mythic rare"
                    rarity = ["rare", "rare", "rare", "rare", "rare", "rare", "rare", "mythic rare"]
                rarity = random.choice(rarity)
            elif rarity[0] == "land"
                rarity = "basic land"
            if rarity != "marketing"
                clean_booster.append(rarity)

    @staticmethod
    def generate_booster(set_code):
        set = Set.get_set_by_code(set_code)
        booster = Set.booster_rarities(json.loads(set['booster']))
        cards = []
        for rarity in booster:
            card_ids_used = [card['id'] for card in cards]
            card = Card.get_random_card(["cards.set_code=%s" % set_code, "cards.rarity=%s" % rarity, "cards.number <= %i" % set['card_count'], "cards.id not in (%s)" % ",".join(list(map(str, card_ids_used)))])
            cards.append(card)
        return cards
