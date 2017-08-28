def insert_card(name,multiverse_id,cmc,color_identity,set_id):
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO cards (name,multiverse_id,cmc,color_identity,set_id) VALUES (?,?,?,?,?)", (name,multiverse_id,cmc,color_identity,set_id))
    con.commit()

def select_card(params=()):
  with sql.connect("database.db") as con:
    cur = con.cursor()
    if params==():
      cur.execute("select * from cards")
    else:
      string = "select"
      for i in xrange(len(params)-1):
        string += "%s,"
      string += "%s"
      string += " from cards"

      result = cur.execute(string)
      return result.fetchall()

def delete_card(params=()):
  with sql.connect("database.db") as con:
    cur = con.cursor()
    if params!=():
      string = "select"
      for i in xrange(len(params)-1):
          string += "%s,"
      string += "%s"
      string += " from cards"

      result = cur.execute(string)
      return result.fetchall()