"""
 Simple API endpoint for returning sets
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)

sets = Blueprint('sets', __name__, url_prefix='/api/v1/sets')

@sets.route('/', methods=['GET'])
def get_sets():
    sets = select_items('sets', ())
    return jsonify(sets), 201
