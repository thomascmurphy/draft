import sqlite3 as sql
from flask import current_app

def insert_item(model, values):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    fields = ','.join(list(values.keys()))
    values = ','.join(list(values.values()))
    cur.execute("INSERT INTO %s (%s) VALUES (%s)", (model, fields, values))
    result = con.commit()
  return result

def select_items(model, params=()):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    if params==():
      result = cur.execute("select * from %s" % model)
    else:
      query = "select * from %s where " % model
      query += ' & '.join(params)
      result = cur.execute(query).fetchall()
  return result

def update_item(model, values, params=()):
  with sql.connect(current_app.config['DATABASE']) as con:
    cur = con.cursor()
    updates = ', '.join(values)
    if params==():
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
