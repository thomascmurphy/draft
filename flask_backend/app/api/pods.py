"""
 Simple API endpoint for returning pods
"""
import ast
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from ..models import Pod, Pack, PackCard

pods = Blueprint('pods', __name__, url_prefix='/api/v1/pods')
import pdb

@pods.route('/', methods=['GET'])
def get_pods():
    pods = Pod.get_pods([])
    return jsonify({'pods': pods}), 201

@pods.route('/<int:pod_id>', methods=['GET'])
def get_pod(pod_id):
    pod = Pod.get_pod_by_id(pod_id)
    return jsonify({'pod': pod}), 201

@pods.route('/', methods=['POST'])
def create_pod():
    name = request.form['name']
    pack_sets = request.form['pack_sets']
    player_emails = ast.literal_eval(request.form['player_emails'])
    pod = Pod.create_pod(name, pack_sets, player_emails)
    return jsonify(pod), 201

@pods.route('/<int:pod_id>', methods=['DELETE'])
def delete_pod(pod_id):
    pod = Pod.delete_pod(pod_id)
    return jsonify(pod), 201

@pods.route('/<int:pod_id>/picks', methods=['POST'])
def create_pick():
    pick = PackCard.update_pack_cards(xxxx)
    return jsonify(pick), 201

@pods.route('/<int:pod_id>/pack/<int:pack_number>/picks', methods=['GET'])
def view_picks():
    pod = Pod.get_pod_by_id(pod_id)
    packs = Pack.get_packs(["pod_id=%i" % pod_id, "order=%i" % pack_number])
    picks = PackCard.get_pack_cards(xxxx)
    return jsonify(picks), 201
