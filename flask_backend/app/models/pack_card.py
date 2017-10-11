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
    def pick_pack_card(pack_card_id, deck_id, player_id, next_player_id, pick_number, pack_player_id, pod_id):
        if player_id == pack_player_id:
          pack_card = PackCard.update_pack_card_by_id(pack_card_id, ['pick_number=%i' % pick_number, 'deck_id=%i' % deck_id])
          remaining_cards = select_items('pack_cards', ['pack_id=%i' % pack_card['pack_id'], 'deck_id IS NULL'])
          pack_complete = 0 if len(remaining_cards) > 0 else 1
          update = update_item('packs', ['player_id=%i' % next_player_id, 'complete=%i' % pack_complete], ['packs.id=%i' % pack_card['pack_id']])
          if pack_complete:
            pack = select_item_by_id('packs', pack_card['pack_id'])
            if pack['number'] < 3:
              next_pack = update_item('packs', ['open=1'], ['packs.player_id=%i' % player_id, 'packs.number=%i' % (pack['number'] + 1)])
            else:
              pod = PackCard.check_pod_completion(pod_id)
          return pack_card

    @staticmethod
    def add_card_data_to_pack_cards(pack_cards):
        card_ids = [pack_card['card_id'] for pack_card in pack_cards]
        cards = select_items('cards', ["cards.id in (%s)" % ",".join(list(map(str, card_ids)))])
        card_data = {card['id']: {'image_url': "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%i&type=card" % card['multiverse_id'], 'cmc': card['cmc'], 'colors': card['colors'], 'mana_cost': card['mana_cost'], 'types': card['types'], 'rating': card['rating']} for card in cards}
        pack_cards = [dict(card_data[pack_card['card_id']], **pack_card) for pack_card in pack_cards]
        return pack_cards

    @staticmethod
    def add_ratings(pack_cards, deck_cards_color_count, deck_cards_cmc_count):
        card_ids = [pack_card['card_id'] for pack_card in pack_cards]
        cards = select_items('cards', ["cards.id in (%s)" % ",".join(list(map(str, card_ids)))])
        ratings = {card['id']: card.calculate_rating(deck_cards_color_count, deck_cards_cmc_count) for card in cards}
        pack_cards = [dict(ratings[pack_card['card_id']], **pack_card) for pack_card in pack_cards]
        return pack_cards

    @staticmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true

    @staticmethod
    def check_pod_completion(pod_id):
      pod = select_item_by_id('pods', pod_id, associations=[{'table': 'players', 'model': 'player', 'join_name': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}])
      player_ids = pod['player_ids']
      unfinished_packs = select_items('packs', ["packs.player_id in (%s)" % ",".join(list(map(str, player_ids))), "complete=0"])
      if len(unfinished_packs) == 0:
        pod_update = update_item('pods', ['complete=1'], ["pods.id=%i" % pod_id])
        return True
      else:
        return False
