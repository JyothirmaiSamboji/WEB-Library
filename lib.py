from sqlite3 import connect
from data import tables

def run_query(cmd):
    with connect ('sqlite.db') as con:
        cur=con.cursor()
        cur.execute(cmd)
        con.commit()
        return cur.fetchall()


    