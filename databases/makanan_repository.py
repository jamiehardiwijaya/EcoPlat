from databases.db import execute_query, fetch_all, fetch_one

class MakananRepository:

    @staticmethod
    def tambah_makanan(data):
        query = """
            INSERT INTO resep (id_user, nama, jumlah, tanggal_kadaluarsa, bahan_utama, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return execute_query(query, (
            data["id_user"],
            data["nama"],
            data["jumlah"],
            data["tanggal_kadaluarsa"],
            data["bahan_utama"],
            data["status"]
        ))
    
    @staticmethod
    def get_by_user(id_user):
        query = "SELECT * FROM sisa_makanan WHERE id_user = ? ORDER BY tanggal_kadaluarsa ASC"
        return fetch_all(query, (id_user,))
    
    @staticmethod
    def get_by_id(id_sisa):
        query = "SELECT * FROM sisa_makanan WHERE id_sisa = ?"
        return fetch_one(query, (id_sisa,))
    
    @staticmethod
    def update_makanan(id_sisa, data):
        query = """
            UPDATE sisa_makanan
            SET nama = ?, jumlah = ?, tanggal_kadaluarsa = ?, bahan_utama = ?, status = ?
            WHERE id_sisa = ?
        """
        return execute_query(query, (
            data['nama'],
            data['jumlah'],
            data['tanggal_kadaluarsa'],
            data['bahan_utama'],
            data['status'],
            id_sisa
        ))
    
    @staticmethod
    def delete_makanan(id_sisa):
        query = "DELETE FROM sisa_makanan WHERE id_sisa = ?"
        return execute_query(query, (id_sisa,))