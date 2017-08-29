"""
 Simple API endpoint for returning sets
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)

sets = Blueprint('sets', __name__, url_prefix='/api/v1/sets')

@sets.route('/', methods=['GET'])
def get_sets():
    sets = Set.all()
    result_json = list(map(lambda set: {'name': set.name, 'code': set.code}, set))
    return jsonify(result_json), 201
