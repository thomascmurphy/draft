def insert_pod(name):
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO pods (name) VALUES (?)", (name))
    con.commit()
