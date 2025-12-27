import sqlite3
import os

db = "ecoplat.db"
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
    
    last_id = c.lastrowid
    
    con.close()
    return last_id  

def fetch_one(query, params=()):
    con = get_db_connection()
    c = con.cursor()
    c.execute(query, params)
    result = c.fetchone()
    con.close()
    return dict(result) if result else None

def fetch_all(query, params=()):
    con = get_db_connection()
    c = con.cursor()
    c.execute(query, params)
    results = c.fetchall()
    con.close()
    return [dict(result) for result in results]

