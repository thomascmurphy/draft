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
    #if model=='cards':
      #pdb.set_trace()
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
