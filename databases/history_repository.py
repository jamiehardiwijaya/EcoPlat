from db import execute_query, fetch_all

def add_history(user_id, sisa_makanan_id, tanggal_kadaluwarsa, jenis_makanan, jumlah, status, nama):
    query = """
        INSERT INTO user_history 
        (user_id, sisa_makanan_id, tanggal_kadaluwarsa, jenis_makanan, jumlah, status, nama)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    execute_query(query, (user_id, sisa_makanan_id, tanggal_kadaluwarsa, jenis_makanan, jumlah, status, nama))

def get_history_by_user(user_id):
    query = "SELECT * FROM user_history WHERE user_id = ?"
    return fetch_all(query, (user_id,))

