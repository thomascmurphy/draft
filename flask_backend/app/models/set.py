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
        if "rare" in rarity and "mythic rare" in rarity:
          rarity = ["rare"] * 7
          rarity.extend(["mythic rare"])
        elif "foil mythic rare" in rarity and "foil rare" in rarity and "foil uncommon" in rarity and "foil common" in rarity:
          rarity = ["common"] * 18
          rarity.extend(["uncommon"] * 12)
          rarity.extend(["rare"] * 5)
          rarity.append("mythic rare")
        rarity = re.sub("foil\s", "", random.choice(rarity))
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
  def seed_data(reseed=False):
    with open('AllSets.json') as sets_file:
      set_data = json.load(sets_file)
    Set.seed_sets(set_data, reseed)
    sets = Set.get_sets([])
    return sets

  @staticmethod
  def seed_sets(set_data, reseed=False):
    included_sets = ["MM3", "AKH", "HOU", "XLN", "IMA", "RIX", "A25", "DOM"]
    for set_code, set in set_data.items():
      existing_sets = Set.get_sets(["code='%s'" % set_code])
      if set['code'] in included_sets:
        if not existing_sets:
          new_set = Set.create_set(set['name'], set_code, json.dumps(set['booster']), set['releaseDate'], len(set['cards']))
        if not existing_sets or reseed:
          Set.seed_cards(set['code'], set['cards'])

  # @staticmethod
  # def seed_lands(set_data):
  #   included_sets = ["ZEN", "UNH", "UGL", "LEA", ""]
  #   zen_full_arts = [195179, 201972, 201974, 195163,   201966, 201964, 201963, 195170,    201977, 201978, 195159, 195157,     201968, 201969, 201970, 201967,    195158, 201962, 201960, 195183]
  #   unh_full_arts = []
  #   ugl_full_arts = []
  #   land_ids = []
  #   for set_code, set in set_data.items():
  #     if set['code'] in included_sets:
  #       lands = [card for card in set['cards'] if card['id'] in land_ids]
  #       Set.seed_cards(set['code'], lands)

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
