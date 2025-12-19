from databases.db import execute_query, fetch_all, fetch_one

class ResepRepository:

    @staticmethod
    def tambah_resep(user_id, nama_resep, deskripsi):
        query = """
        INSERT INTO resep (user_id, nama_resep, deskripsi)
        VALUES (?, ?, ?)
        """
        return execute_query(query, (user_id, nama_resep, deskripsi))

    @staticmethod
    def get_by_user(user_id):
        query = """
        SELECT id, nama_resep, deskripsi
        FROM resep
        WHERE user_id = ?
        """
        return fetch_all(query, (user_id,))

    @staticmethod
    def get_all():
        query = """
        SELECT r.id, r.nama_resep, r.deskripsi, u.nama AS pembuat
        FROM resep r
        JOIN users u ON r.user_id = u.id
        """
        return fetch_all(query)

    @staticmethod
    def delete_resep(resep_id, user_id):
        query = """
        DELETE FROM resep
        WHERE id = ? AND user_id = ?
        """
        execute_query(query, (resep_id, user_id))

    @staticmethod
    def get_resep_by_bahan(bahan_id):
        query = """
        SELECT r.id, r.nama_resep, r.deskripsi
        FROM resep r
        JOIN bahan_resep br ON r.id = br.resep_id
        WHERE br.bahan_id = ?
        """
        return fetch_all(query, (bahan_id,))