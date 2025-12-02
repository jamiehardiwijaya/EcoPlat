import sqlite3
import os

db = "EcoPlat.db"
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db)

def get_db_connection():
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con

def execute_query(query, params=()):
    con = get_db_connection()
    c = con.cursor()
    c.execute(query, params)
    con.commit()
    con.close()

def fetch_one(query, params=()):
    con = get_db_connection()
    c = con.cursor()
    c.execute(query, params)
    result = c.fetchone()
    con.close()
    return result

def fetch_all(query, params=()):
    con = get_db_connection()
    c = con.cursor()
    c.execute(query, params)
    result = c.fetchall()
    con.close()
    return result

