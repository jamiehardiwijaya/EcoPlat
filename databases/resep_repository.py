from databases.db import execute_query, fetch_all, fetch_one

class ResepRepository:

    @staticmethod
    def tambah_resep(data):
        query = """
            INSERT INTO resep (id_user, nama_resep, deskripsi)
            VALUES (?, ?, ?)
        """

        id_resep = execute_query(query, (
            data["id_user"],
            data["nama_resep"],
            data["deskripsi"]
        ))

        for id_bahan in data.get("bahan_dibutuhkan", []):
            query_bahan = """
                INSERT INTO resep_bahan (id_resep, id_bahan)
                VALUES (?, ?)
            """
            execute_query(query_bahan, (id_resep, id_bahan))

        return id_resep
    
    @staticmethod
    def tambah_bahan_ke_resep(id_resep, id_bahan):
        query = """
            INSERT INTO resep_bahan (id_resep, id_bahan)
            VALUES (?, ?)
        """
        return execute_query(query, (id_resep, id_bahan))
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM resep ORDER BY id_resep DESC"
        return fetch_all(query)
    
    @staticmethod
    def get_by_id(id_resep):
        query = "SELECT * FROM resep WHERE id_resep = ?"
        resep = fetch_one(query, (id_resep,))

        if not resep:
            return None
        
        bahan_query = """
            SELECT b.id_bahan, b.nama_bahan
            FROM bahan b
            JOIN resep_bahan rb ON b.id_bahan = rb.id_bahan
            WHERE rb.id_resep = ?
        """

        bahan = fetch_all(bahan_query, (id_resep,))
        resep['bahan_dibutuhkan'] = bahan

        return resep
    
    @staticmethod
    def hapus_resep(id_resep):
        execute_query("DELETE FROM resep_bahan WHERE id_resep = ?", (id_resep,))
        return execute_query("DELETE FROM resep WHERE id_resep = ?", (id_resep,))