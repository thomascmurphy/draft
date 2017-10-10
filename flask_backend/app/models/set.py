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
        set = select_first_item('sets', ["sets.code='%s'" % code])
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
                if rarity[0] == "rare" and rarity[1] == "mythic rare":
                    rarity = ["rare", "rare", "rare", "rare", "rare", "rare", "rare", "mythic rare"]
                rarity = random.choice(rarity)
            elif rarity == "land":
                rarity = "basic land"
            if rarity != "marketing":
                clean_booster.append(rarity)
        return clean_booster

    @staticmethod
    def generate_booster(set_code):
        set_code = set_code.upper()
        set = Set.get_set_by_code(set_code)
        booster = Set.booster_rarities(set['booster'])
        cards = []
        for rarity in booster:
            card_ids_used = [card['id'] if card and 'id' in card else 0 for card in cards]
            card = Card.get_random_card(["cards.set_code='%s'" % set_code, "cards.rarity='%s'" % rarity, "cards.number <= %i" % set['card_count'], "cards.id not in (%s)" % ",".join(list(map(str, card_ids_used)))])
            cards.append(card)
        return cards

    @staticmethod
    def seed_data():
      with open('AllSets.json') as sets_file:
        set_data = json.load(sets_file)
      Set.seed_sets(set_data)
      sets = Set.get_sets([])
      return sets

    @staticmethod
    def seed_sets(set_data):
      for set_code, set in set_data.items():
        existing_sets = Set.get_sets(["code='%s'" % set_code])
        included_sets = ["MM3", "AKH", "HOU", "XLN", "IMA"]
        if set['code'] in included_sets:
          if not existing_sets:
              new_set = Set.create_set(set['name'], set_code, json.dumps(set['booster']), set['releaseDate'], len(set['cards']))
          Set.seed_cards(set['code'], set['cards'])

    @staticmethod
    def seed_cards(set_code, card_data):
      for card in card_data:
        existing_cards = Card.get_cards(["multiverse_id=%s" % card['multiverseid']])
        colors = json.dumps(card['colors']) if 'colors' in card else '[]'
        mana_cost = card['manaCost'] if 'manaCost' in card else ''
        number = int(re.sub("[^0-9]", "", card['number']))
        if not existing_cards:
          new_card = Card.create_card(card['name'], card['multiverseid'], card['cmc'], colors, set_code, mana_cost, json.dumps(card['types']), card['rarity'].lower(), number)
        elif not existing_cards[0]['colors'] or not existing_cards[0]['types'] or not existing_cards[0]['rarity'] or not existing_cards[0]['number']:
          update_card = update_item('cards', ["colors='%s'" % colors, "types='%s'" % json.dumps(card['types']), "rarity='%s'" % card['rarity'].lower(), "number=%i" % number], params=["id=%i" % existing_cards[0]['id']])
