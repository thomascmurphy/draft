import sqlite3 as sql
from flask import current_app
import pdb

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

def select_items(model, params=[]):
  with sql.connect(current_app.config['DATABASE']) as con:
    con.row_factory = sql.Row
    cur = con.cursor()
    if params==[]:
      result = cur.execute("select * from %s" % model).fetchall()
    else:
      query = "select * from %s where " % model
      query += ' & '.join(params)
      result = cur.execute(query).fetchall()
    columns = [column[0] for column in cur.description]
    pretty_results = []
    for row in result:
      pretty_results.append(dict(zip(columns, row)))
  return pretty_results

def update_item(model, values, params=[]):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    updates = ', '.join(values)
    if params==[]:
      query = ""
    else:
      query = "where "
      query += ' & '.join(params)
    cur.execute("UPDATE %s SET %s WHERE %s", (model, updates, query))
    result = con.commit()
  return result

def delete_item_with_id(model, id):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    if id != null:
      result = cur.execute("delete from %s where id = %i;" % (model, id))
  return result
