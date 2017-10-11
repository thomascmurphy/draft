from .models import *
from .player import Player
from .pack import Pack

class Pod():
    #methods
    @staticmethod
    def get_pods(params):
        select_fields = ["pods.id", "pods.name", "pods.pack_1_set", "pods.pack_2_set", "pods.pack_3_set", "pods.complete"]
        pods = select_items('pods', params, select=select_fields, associations=[{'table': 'players', 'join_name': 'player', 'model': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}], group_by='pods.id', order=['id DESC'])
        return pods

    @staticmethod
    def get_pod_by_id(id):
        select_fields = ["pods.id", "pods.name", "pods.pack_1_set", "pods.pack_2_set", "pods.pack_3_set", "pods.complete"]
        pod = select_item_by_id('pods', id, select=select_fields, associations=[{'table': 'players', 'model': 'player', 'join_name': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}])
        return pod

    @staticmethod
    def create_pod(name, pack_1_set, pack_2_set, pack_3_set, players):
        pod = insert_item('pods', {'name': name, 'pack_1_set': pack_1_set, 'pack_2_set': pack_2_set, 'pack_3_set': pack_3_set})
        packs_array = [pack_1_set, pack_2_set, pack_3_set]
        for player_info in players:
            player = Player.create_player(player_info['email'].lower(), player_info['name'], pod['id'])
            for counter,set_code in enumerate(packs_array):
                pack = Pack.create_pack(set_code, player['id'], counter+1, counter==0)
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
        pod = delete_item_with_id('pods', "id='%i'" % id)
        return true
