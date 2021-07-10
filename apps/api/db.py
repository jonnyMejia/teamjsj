# Python Libraries
import psycopg2

from .settings import (
    DB_NAME,
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
)

class Database:

    def __init__(self, dbname=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port,
                                   user=self.user, password=self.passwd)
        self.cur =  self.conn.cursor()
        
    def close(self):
        self.cur.close()
        self.conn.close()