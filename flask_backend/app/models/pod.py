from .models import *
from .player import Player
from .pack import Pack

class Pod():
    #methods
    @staticmethod
    def get_pods(params):
      pods = select_items('pods', params, associations=[{'table': 'players', 'join_name': 'player', 'model': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}], group_by='pods.id', order=['pods.id DESC'])
      return pods

    @staticmethod
    def get_pod_by_id(id):
      pod = select_item_by_id('pods', id, associations=[{'table': 'players', 'model': 'player', 'join_name': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}])
      return pod

    @staticmethod
    def get_pod_by_id_with_players(id):
      pod = Pod.get_pod_by_id(id)
      players = Player.get_players(["players.id in (%s)" % ",".join(list(map(str, pod['player_ids'])))], associations=[{'table': 'packs', 'join_name': 'pack', 'model': 'pack', 'join_field_left': 'id', 'join_field_right': 'player_id', 'join_filter': 'AND pack.open=1 AND pack.complete=0'}], group_by='players.id')
      pod['players'] = players
      return pod

    @staticmethod
    def create_pod(name, pack_1_set, pack_2_set, pack_3_set, players):
      pod = insert_item('pods', {'name': name, 'pack_1_set': pack_1_set, 'pack_2_set': pack_2_set, 'pack_3_set': pack_3_set})
      packs_array = [pack_1_set, pack_2_set, pack_3_set]
      pod_players = []
      for index, player_info in enumerate(players):
        player_name = player_info['name'] if 'name' in player_info else player_info['email'].lower()
        player = Player.create_player(player_info['email'].lower(), player_name, player_info['is_bot'], index==0, pod['id'])
        pod_players.append(player)
        for counter,set_code in enumerate(packs_array):
          pack = Pack.create_pack(set_code, player['id'], counter+1, counter==0)
      for pod_player in pod_players:
        if pod_player['is_bot']:
          Player.auto_pick_card(pod_player)
      return pod

    @staticmethod
    def update_pods(values, params):
      pod_update = update_item('pods', values, params)
      pod = select_first_item('pods', params)
      return pod

    @staticmethod
    def update_pod_by_id(id, values):
      return Pod.update_pods(values, ["pods.id=%i" % id])

    @staticmethod
    def delete_pod(id):
      pod = delete_item_with_id('pods', id)
      return True
