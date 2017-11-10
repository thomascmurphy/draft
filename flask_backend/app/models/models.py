from __future__ import print_function # In python 2.7
import sqlite3 as sql
from flask import current_app, jsonify
import pdb
import sys
import ast
import random
import json
import re

def insert_item(model, data):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    fields = ','.join(list(data.keys()))
    values = ','.join(str(v) for v in list(data.values()))
    cur.execute("INSERT INTO %s (%s) VALUES (%s)" % (model, fields, ','.join('?' * len(data.values()))), list(data.values()))
    result = {'id': cur.lastrowid}
    result.update(data)
    con.commit()
  return result

def select_items(model, params=[], order=[], select=[], associations=[], group_by='', limit=''):
  with sql.connect(current_app.config['DATABASE']) as con:
    con.row_factory = sql.Row
    cur = con.cursor()

    if select == []:
      select = ["%s.*" % model]

    if associations!=[]:
      id_fields = ["'[' || group_concat(%s.id) || ']' AS %s_ids" % (association['join_name'], association['join_name']) for association in associations]
      joins = ["LEFT JOIN %s %s ON (%s.%s = %s.%s %s)" % (association['table'], association['join_name'], model, association['join_field_left'], association['join_name'], association['join_field_right'], association['join_filter']) for association in associations]
      select += id_fields
      join_query = " " + " ".join(joins)
    else:
      join_query = ''


    query = "SELECT %s FROM %s" % (','.join(select), model)
    query += join_query

    if params!=[]:
      query += " WHERE " + ' AND '.join(params)
    if group_by != '':
      query += " GROUP BY %s " % group_by
    if order != []:
      query += " ORDER BY " + ', '.join(order)
    if limit != '':
      query += " LIMIT %i" % limit
    #print(query, file=sys.stderr)
    result = cur.execute(query).fetchall()
    columns = [column[0] for column in cur.description]
    pretty_results = []
    for row in result:
      if set(dict(row).values()) != {None}:
        #pretty_results.append(dict(zip(columns, row)))
        dict_row = {k: json.loads(v) if (isinstance(v, str) and len(v) > 0 and v[0] == '[') else v for k, v in dict(row).items()}
        pretty_results.append(dict_row)
  return pretty_results

def select_item_by_id(model, id, associations=[]):
  return select_first_item(model, ["%s.id = %i" % (model, id)], associations=associations)

def select_first_item(model, params=[], order=[], select=[], associations=[], group_by=''):
    items = select_items(model, params, order, select, associations, group_by, 1)
    if items:
      item = items[0]
    else:
      item = None
    return item


def update_item(model, values, params=[]):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    updates = ', '.join(values)
    if params==[]:
      query = ""
    else:
      query = ' AND '.join(params)

    #print("UPDATE %s SET %s WHERE %s" % (model, updates, query), file=sys.stderr)
    result = cur.execute("UPDATE %s SET %s WHERE %s" % (model, updates, query))
    con.commit()
  return result

def delete_item_with_id(model, id):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    if id != None:
      result = cur.execute("delete from %s where id = %i" % (model, id))
  return result



def check_pod_completion(pod_id):
  pod = select_item_by_id('pods', pod_id, associations=[{'table': 'players', 'model': 'player', 'join_name': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}])
  player_ids = pod['player_ids']
  unfinished_packs = select_items('packs', ["packs.player_id in (%s)" % ",".join(list(map(str, player_ids))), "complete=0"])
  if len(unfinished_packs) == 0:
    pod_update = update_item('pods', ['complete=1'], ["pods.id=%i" % pod_id])
    return True
  else:
    return False

def check_all_packs_completion(pod_id, pack_number):
  pod = select_item_by_id('pods', pod_id, associations=[{'table': 'players', 'model': 'player', 'join_name': 'player', 'join_field_left': 'id', 'join_field_right': 'pod_id', 'join_filter': ''}])
  player_ids = pod['player_ids']
  unfinished_packs = select_items('packs', ["packs.player_id in (%s)" % ",".join(list(map(str, player_ids))), "complete=0", "number=%i" % pack_number])
  if len(unfinished_packs) == 0:
    if pack_number < 3:
      next_pack = update_item('packs', ['open=1'], ["packs.player_id in (%s)" % ",".join(list(map(str, player_ids))), 'packs.number=%i' % (pack_number + 1)])
    else:
      check_pod_completion(pod_id)
    return True
  else:
    return False

def calculate_card_rating(card, deck_cards_color_count, deck_cards_cmc_count):
  base_rating = card['rating'] if card['rating'] else 0
  cmc = card['cmc']
  cmc_size = deck_cards_cmc_count[str(cmc)] if str(cmc) in deck_cards_cmc_count else 0
  symbols = re.findall(r'\{.+\}', card['mana_cost'])
  colors = card['colors']
  deck_card_count = sum(deck_cards_cmc_count.values())
  cast_rating = 0
  color_rating = 0
  curve_rating = 0
  if card['types'] != ['Land']:
    cast_rating = 50 / (len(colors) + len(symbols)**2 + cmc**2 + 5)
    if sorted(deck_cards_color_count.values(), reverse=True)[0] > 2 and sorted(deck_cards_color_count.values(), reverse=True)[1] > 2:
      for color in colors:
        color_rating += (50 * deck_cards_color_count[color.lower()] / (deck_card_count + 10) )
      color_rating = color_rating / len(colors) if colors else 5
    if deck_card_count > 8:
      curve_rating = 5 * ((deck_card_count + 1) / (cmc_size + 1)) / (abs(cmc - 2)**1.5 + 5)
  return {'overall_rating': base_rating + cast_rating + color_rating + curve_rating, 'base_rating': base_rating, 'cast_rating': cast_rating, 'color_rating': color_rating, 'curve_rating': curve_rating}

def add_ratings_to_pack_cards(pack_cards, deck_cards_color_count, deck_cards_cmc_count):
  card_ids = [pack_card['card_id'] for pack_card in pack_cards]
  cards = select_items('cards', ["cards.id in (%s)" % ",".join(list(map(str, card_ids)))])
  ratings = {card['id']: calculate_card_rating(card, deck_cards_color_count, deck_cards_cmc_count) for card in cards}
  pack_cards = [dict(ratings[pack_card['card_id']], **pack_card) for pack_card in pack_cards]
  return pack_cards
