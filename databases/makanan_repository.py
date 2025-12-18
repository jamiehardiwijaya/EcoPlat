from databases.db import execute_query, fetch_all, fetch_one

class MakananRepository:

    @staticmethod
    def tambah_makanan(user_id ,nama, jumlah, tanggal_kadaluarsa, kategori):
        query = """
            INSERT INTO sisa_makanan (user_id, nama_makanan, jumlah, tanggal_kadaluarsa, kategori)
            VALUES (?, ?, ?, ?, ?)
        """
        return execute_query(query, (
            user_id ,nama, jumlah, tanggal_kadaluarsa, kategori
        ))
    
    @staticmethod
    def get_by_user(user):
        query = "SELECT * FROM sisa_makanan WHERE user_id = ? ORDER BY tanggal_kadaluarsa ASC"
        return fetch_all(query, (user,))
    
    @staticmethod
    def get_by_id(id_sisa):
        query = "SELECT * FROM sisa_makanan WHERE id = ?"
        return fetch_one(query, (id_sisa,))
    
    @staticmethod
    def update_makanan(id_sisa, nama, jumlah, tanggal_kadaluarsa, kategori):
        query = """
            UPDATE sisa_makanan
            SET nama_makanan = ?, jumlah = ?, tanggal_kadaluarsa = ?, kategori = ?
            WHERE id = ?
        """
        return execute_query(query, (
            nama, jumlah, tanggal_kadaluarsa, kategori, id_sisa
        ))
    
    @staticmethod
    def delete_makanan(id):
        query = "DELETE FROM sisa_makanan WHERE id = ?"
        return execute_query(query, (id,))