from .models import *

class Pack():
    #methods
    @classmethod
    def get_packs(params):
        packs = select_items('packs', params)
        return packs

    @classmethod
    def get_pack_by_id(id):
        pack = select_items('packs', "id='%i'" % id)[0]
        return pack

    @classmethod
    def create_pack(params):
        pack = insert_item('packs', params)
        return pack

    @classmethod
    def delete_pack(id):
        pack = delete_item_with_id('packs', "id='%i'" % id)
        return true
