import sqlite3 as sql

def insert_item(model, values):
  with sql.connect(app.config['DATABASE']) as con:
    cur = con.cursor()
    fields = ','.join(list(values.keys()))
    values = ','.join(list(values.values()))
    cur.execute("INSERT INTO %s (%s) VALUES (%s)", (model, fields, values))
    result = con.commit()
  return result

def select_items(model, params=()):
  with sql.connect(app.config['DATABASE']) as con:
    cur = con.cursor()
    if params==():
      cur.execute("select * from %s" % model)
    else:
      query = "select * from %s where " % model
      query += ' & '.join(params)
      result = cur.execute(query).fetchall()
  return result

def delete_pod_with_id(model, id):
  with sql.connect(app.config['DATABASE']) as con:
    cur = con.cursor()
    if id != null
      result = cur.execute("delete from %s where id = %i;" % (model, id))
  return result
