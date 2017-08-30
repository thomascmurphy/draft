"""
 Simple API endpoint for returning pods
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from ..models import Pod, PackCard

pods = Blueprint('pods', __name__, url_prefix='/api/v1/pods')

@pods.route('/', methods=['GET'])
def get_pods():
    pods = Pod.get_pods()
    return jsonify(pods), 201

@pods.route('/<int:pod_id>', methods=['GET'])
def get_pod(pod_id):
    pods = Pod.get_pod_by_id(pod_id)
    return jsonify(pods), 201

@pods.route('/', methods=['POST'])
def create_pod():
    pod = Pod.create_pod(request.params)
    return jsonify(pod), 201

@pods.route('/<int:pod_id>', methods=['DELETE'])
def delete_pod(pod_id):
    pod = Pod.delete_pod(pod_id)
    return jsonify(pod), 201

@pods.route('/<int:pod_id>/picks', methods=['POST'])
def create_pick():
    pick = PackCard.update_pack_card(xxxx)
    return jsonify(pick), 201

@pods.route('/<int:pod_id>/picks', methods=['GET'])
def view_picks():
    picks = PackCard.get_pack_cards(xxxx)
    return jsonify(picks), 201
