from databases.db import fetch_all, fetch_one, execute_query

class BahanRepository:

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM bahan")

    @staticmethod
    def get_by_name(nama):
        return fetch_one("SELECT * FROM bahan WHERE nama = ?", (nama,))

    @staticmethod
    def tambah_bahan(nama):
        return execute_query(
            "INSERT INTO bahan (nama) VALUES (?)",
            (nama,)
        )