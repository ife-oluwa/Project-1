from sqllite import sqllite_db

db = sqllite_db('ESTATE')

conn = db.get_connection()
c = conn.cursor()
items = c.execute('''SELECT * FROM ESTATE''')
count = len(items.fetchall())
print(count)
conn.commit()
conn.close()
