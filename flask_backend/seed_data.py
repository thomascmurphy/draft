import json
from app.models import Set, Card

def seed_sets(set_data):
    for set in set_data:
        existing_sets = Set.get_sets(["code=%s" % set['code']])
        included_sets = ["MM3", "AKH", "HOU", "XLN", "IMA"]
        if not existing_sets and set['code'] in included_sets:
            new_set = Set.create_set(set['name'], set['code'], json.dumps(set['booster']), set['releaseDate'], len(set['cards']))
        seed_cards(set['code'], set['cards'])

def seed_cards(set_code, card_data):
    for card in card_data:
        existing_cards = Card.get_cards(["multiverse_id=%s" % card['multiverseid']])
        if not existing_cards:
            new_card = Card.create_card(card['name'], card['multiverseid'], card['cmc'], json.dumps(card['colorIdentity']), set_code, card['manaCost'], json.dumps(card['types']), card['rarity'].lower(), card['number'])
        if not existing_cards[0]['types'] or not existing_cards[0]['rarity'] or not existing_cards[0]['number']:
            update_card = update_item('cards', ["types=%s" % existing_cards[0]['types'], "rarity=%s" % existing_cards[0]['rarity'].lower(), "number=%s" % existing_cards[0]['number']], params=["id=%i" % existing_cards[0]['id']])

with open('AllSets.json') as sets_file:
    set_data = json.load(sets_file)

seed_sets(set_data)
