from db import execute_query, fetch_all, fetch_one

def tambah_rekomendasi(makanan_id, resep_id):
    query = """
        INSERT INTO rekomendasi_resep (makanan_id, resep_id)
        VALUES (?, ?)
    """
    execute_query(query, (makanan_id, resep_id))


def get_rekomendasi_by_makanan(makanan_id):
    query = """
        SELECT resep.* 
        FROM rekomendasi_resep 
        JOIN resep ON resep.id_resep = rekomendasi_resep.resep_id
        WHERE rekomendasi_resep.makanan_id = ?
    """
    return fetch_all(query, (makanan_id,))


def hapus_rekomendasi(makanan_id, resep_id):
    query = """
        DELETE FROM rekomendasi_resep
        WHERE makanan_id = ? AND resep_id = ?
    """
    execute_query(query, (makanan_id, resep_id))


def sudah_ada_rekomendasi(makanan_id, resep_id):
    query = """
        SELECT * FROM rekomendasi_resep
        WHERE makanan_id = ? AND resep_id = ?
    """
    row = fetch_one(query, (makanan_id, resep_id))
    return row is not None