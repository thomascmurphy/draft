def insert_card(name,image_url,multiverse_id,cmc,color_identity,set_id):
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO cards (name,image_url,multiverse_id,cmc,color_identity,set_id) VALUES (?,?,?,?,?,?)", (name,image_url,multiverse_id,cmc,color_identity,set_id))
    con.commit()
