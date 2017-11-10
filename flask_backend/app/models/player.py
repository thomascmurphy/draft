import base64
from flask import current_app

from .models import *
from .pack import Pack
from .deck import Deck
from .pack_card import PackCard

class Player():
    #methods
    @staticmethod
    def get_players(params, associations=[], group_by=''):
      players = select_items('players', params, associations=associations, group_by=group_by)
      return players

    @staticmethod
    def get_player_by_hash(hash):
      #cipher = AES.new(current_app.config['PLAYER_HASH_KEY'])
      #hash = base64.encodestring(cipher.encrypt("%016d"%id))
      #id = int(cipher.decrypt(base64.decodestring(hash)))
      email = base64.b64decode(hash)
      player = select_first_item('players', ["hash='%s'" % hash])
      return player

    @staticmethod
    def get_player_by_id(id):
      player = select_item_by_id('players', id)
      return player

    @staticmethod
    def create_player(email, name, is_bot, is_owner, pod_id):
      player_identifier = email if not is_bot else name
      hash_components = "%i%s" % (pod_id, player_identifier)
      player_hash = base64.b64encode(hash_components.encode())
      player_hash_string = player_hash.decode('utf-8')
      player = insert_item('players', {'email': email, 'name': name, 'is_bot': is_bot, 'pod_id': pod_id, 'hash': player_hash_string, 'is_owner': is_owner})
      deck = Deck.create_deck(player['id'])
      return player

    @staticmethod
    def delete_player(id):
      player = delete_item_with_id('players', "id='%i'" % id)
      return true

    @staticmethod
    def get_player_pack(player_id):
      packs = select_items('packs', ["player_id = %i" % player_id, "complete = 0", "open = 1"], ['number ASC'], associations=[{'table': 'pack_cards', 'join_name': 'pack_card', 'model': 'pack_card', 'join_field_left': 'id', 'join_field_right': 'pack_id', 'join_filter': 'AND pack_card.deck_id IS NULL'}], group_by='packs.id')
      if packs:
        pack = sorted(packs, key=lambda pack: (pack['number'], -len(pack['pack_card_ids'])))[0]
      else:
        pack = None
      return pack

    @staticmethod
    def get_player_deck(player_id):
      deck = select_first_item('decks', ["player_id=%i" % player_id])
      return deck

    @staticmethod
    def pick_pack_card(pack_card_id, deck_id, player_id, next_player, pick_number, pack_player_id, pod_id):
      if player_id == pack_player_id:
        pack_cards_update = update_item('pack_cards', ['pick_number=%i' % pick_number, 'deck_id=%i' % deck_id], ["pack_cards.id=%i" % pack_card_id])
        pack_card = select_first_item('pack_cards', ["pack_cards.id=%i" % pack_card_id])
        remaining_cards = select_items('pack_cards', ['pack_id=%i' % pack_card['pack_id'], 'deck_id IS NULL'])
        pack_complete = 0 if len(remaining_cards) > 0 else 1
        update = update_item('packs', ['player_id=%i' % next_player['id'], 'complete=%i' % pack_complete], ['packs.id=%i' % pack_card['pack_id']])
        if pack_complete:
          pack = select_item_by_id('packs', pack_card['pack_id'])
          crack_next_packs = check_all_packs_completion(pod_id, pack['number'])
        if next_player['is_bot']:
          Player.auto_pick_card(next_player)
        return pack_card

    @staticmethod
    def auto_pick_card(player):
      pack = Player.get_player_pack(player['id'])
      if pack:
        deck = Player.get_player_deck(player['id'])
        pack_cards = Pack.get_available_cards(pack['id'])
        deck_stats = Deck.get_stats(deck['id'])
        pack_cards = add_ratings_to_pack_cards(pack_cards, deck_stats['deck_cards_color_count'], deck_stats['deck_cards_cmc_count'])
        pick = sorted(pack_cards, key=lambda pack_cards: -pack_cards['overall_rating'])[0]
        pod = select_item_by_id('pods', player['pod_id'], associations=[{'table': 'players', 'model': 'player', 'join_name': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}])
        player_ids = pod['player_ids']
        next_player_modifier = -1 if pack['number'] == 2 else 1
        next_player_id = player_ids[(player_ids.index(player['id']) + next_player_modifier)%len(player_ids)]
        next_player = Player.get_player_by_id(next_player_id)
        pick_number = deck_stats['deck_cards_count'] + 1
        return Player.pick_pack_card(pick['id'], deck['id'], player['id'], next_player, pick_number, pack['player_id'], pod['id'])
      else:
        return False

    @staticmethod
    def auto_build_deck(player):
      deck = Player.get_player_deck(player['id'])
      deck_stats = Deck.get_stats(deck['id'])
      deck_cards = add_ratings_to_pack_cards(select_items('pack_cards', ["deck_id=%i" % deck['id']]), deck_stats['deck_cards_color_count'], deck_stats['deck_cards_cmc_count'])
      viable_colors = [color for color,count in enumerate(deck_stats['deck_cards_color_count']) if count > 4]
      viable_cards = [deck_card for deck_card in deck_cards if deck_card['colors'] == [] or len(list(filter(lambda x: x in [color.lower() for color in deck_card['colors']], viable_colors))) > 0]
      picks = sorted(viable_cards, key=lambda viable_cards: -viable_cards['overall_rating'])[:23]
      pick_ids = [pick['id'] for pick in picks]
      pick_updates = update_item('pack_cards', ['sideboard=0'], ["id in (%s)" % ",".join(list(map(str, pick_ids)))])
      nonland_picks = [pick for pick in picks if pick['types'] != ["Land"]]
      return True
