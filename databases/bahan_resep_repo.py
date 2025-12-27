from databases.db import execute_query, fetch_all

class BahanResepRepository:

    @staticmethod
    def tambah(resep_id, bahan_id):
        query = """
        INSERT INTO bahan_resep (resep_id, bahan_id)
        VALUES (?, ?)
        """
        execute_query(query, (resep_id, bahan_id))

    @staticmethod
    def get_bahan_by_resep(resep_id):
        query = """
        SELECT b.nama
        FROM bahan b
        JOIN bahan_resep br ON b.id = br.bahan_id
        WHERE br.resep_id = ?
        """
        return fetch_all(query, (resep_id,))