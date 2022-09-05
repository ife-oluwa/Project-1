import sqlite3


class sqllite_db(object):
    def __init__(self, table='ESTATE'):
        self.table = table

    def get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('metroscubicos.sqlite')
        except sqlite3.error as e:
            print(e)
        return conn

    def init_table(self):
        con = self.get_connection()
        c = con.cursor()
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table}
            (propertyName TEXT,
            url TEXT,
            address TEXT,
            street TEXT,
            number TEXT,
            settlement TEXT,
            town TEXT,
            state TEXT,
            county TEXT,
            description TEXT,
            amenities TEXT,
            size TEXT,
            firstPicture TEXT)''')
        con.commit()
        con.close()

    def bulk_data(self, data):
        data.to_sql(self.table, con=self.get_connection(), if_exists="replace")

    def validate(self):
        con = self.get_connection()
        c = con.cursor()
        items = c.execute('''
            SELECT * FROM ESTATE''')
        count = len(items.fetchall())
        con.commit()
        con.close()
        return count
