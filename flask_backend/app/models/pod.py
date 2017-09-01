import ast

from .models import *
from .player import Player
from .pack import Pack
import pdb

fields = ['name', 'pack_sets']

class Pod():
    #methods
    @staticmethod
    def get_pods(params):
        pods = select_items('pods', params)
        return pods

    @staticmethod
    def get_pod_by_id(id):
        pod = select_items('pods', ["id=%i" % id])[0]
        return pod

    @staticmethod
    def create_pod(name, pack_sets, player_emails):
        # clean_params_pod = {field:params[field] for param in fields}
        pod = insert_item('pods', {'name': name, 'pack_sets': pack_sets})
        packs_array = ast.literal_eval(pack_sets)
        for player_email in player_emails:
            player = Player.create_player(player_email, pod['id'])
            for counter,set_code in enumerate(packs_array):
                pack = Pack.create_pack(set_code, player['id'], counter+1)
        return pod

    @staticmethod
    def delete_pod(id):
        pod = delete_item_with_id('pods', "id='%i'" % id)
        return true
