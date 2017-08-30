from .models import *

class Pod():
    #methods
    @classmethod
    def get_pods(params):
        pods = select_items('pods', params)
        return pods

    @classmethod
    def get_pod_by_id(id):
        pod = select_items('pods', "id='%i'" % id)[0]
        return pod

    @classmethod
    def create_pod(params):
        pod = insert_item('pods', params)
        return pod

    @classmethod
    def delete_pod(id):
        pod = delete_item_with_id('pods', "id='%i'" % id)
        return true
