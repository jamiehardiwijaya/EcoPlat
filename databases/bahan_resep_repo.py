from databases.db import execute_query, fetch_all

class BahanResepRepository:

    @staticmethod
    def tambah(resep_id, bahan_id):
        query = """
        INSERT INTO bahan_resep (resep_id, bahan_id)
        VALUES (?, ?)
        """
        execute_query(query, (resep_id, bahan_id))