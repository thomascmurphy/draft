"""
 Simple API endpoint for returning pods
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)

pods = Blueprint('pods', __name__, url_prefix='/api/v1/pods')

@pods.route('/', methods=['GET'])
def get_pods():
    pods = select_items('pods', ())
    return jsonify(pods), 201

@pods.route('/<int:pod_id>', methods=['GET'])
def get_pod(pod_id):
    pods = select_items('pods', ("id=%i" % pod_id))
    return jsonify(pods), 201

@pods.route('/', methods=['POST'])
def create_pod():
    pods = select_items('pods', ())
    return jsonify(pods), 201

@pods.route('/<int:pod_id>', methods=['DELETE'])
def delete_pod(pod_id):
    pods = delete_item_with_id('pods', pod_id)
    return jsonify(pods), 201

@pods.route('/<int:pod_id>/picks', methods=['POST'])
def create_pick():
    pods = select_items('pods', ())
    return jsonify(pods), 201

@pods.route('/<int:pod_id>/picks', methods=['GET'])
def view_picks():
    pods = select_items('pods', ())
    return jsonify(pods), 201
