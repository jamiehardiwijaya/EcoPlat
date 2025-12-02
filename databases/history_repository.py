from db import get_db_connection

def get_history(user_id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM user_history WHERE user_id = ?", (user_id,))
    result = cur.fetchall()
    con.close()
    return result

