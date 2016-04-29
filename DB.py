import psycopg2


class DB:
    def __init__(self, db_name):
        try:
            self.conn = psycopg2.connect("dbname='%s'" % db_name)
        except:
            print "I am unable to connect to the database"
            exit()
        self.cur = self.conn.cursor()

    def cursor(self):
        return self.cur

    def getNewCursor(self):
        return self.conn.cursor()

    def connection(self):
        return self.conn

    def query(self, q):
        self.cur.execute(q)
        return self.cur.fetchall()


def main():
    db1 = DB('tweets')
    q = 'select * from full_tweets limit 1'
    print 'TWEETS DB', db1.query(q)

    db1 = DB('imdb')
    q = 'select * from actors limit 1'
    print 'IMDB DB', db1.query(q)

    print 'Success!'


if __name__ == '__main__':
    main()
