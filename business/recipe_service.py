from databases.resep_repository import ResepRepository
from databases.bahan_repository import BahanRepository
from databases.bahan_resep_repo import BahanResepRepository
from state import AppState

class RecipeService:

    @staticmethod
    def tambah_resep(nama_resep, deskripsi, daftar_bahan):
        user_id = AppState.get_user_id()

        if not user_id:
            return {"success": False, "message": "Anda belum login"}

        if not nama_resep:
            return {"success": False, "message": "Nama resep wajib diisi"}

        try:
            resep_id = ResepRepository.tambah_resep(
                user_id, nama_resep, deskripsi
            )

            for nama in daftar_bahan:
                bahan = BahanRepository.get_by_name(nama)

                if bahan:
                    bahan_id = bahan["id"]
                else:
                    bahan_id = BahanRepository.tambah_bahan(nama)

                BahanResepRepository.tambah(resep_id, bahan_id)

            return {"success": True, "message": "Resep & bahan berhasil disimpan"}

        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def lihat_resep_saya():
        user_id = AppState.get_user_id()
        return ResepRepository.get_by_user(user_id)

    @staticmethod
    def lihat_semua_resep():
        return ResepRepository.get_all()

    @staticmethod
    def hapus_resep(resep_id):
        user_id = AppState.get_user_id()

        try:
            ResepRepository.delete_resep(resep_id, user_id)
            return {"success": True, "message": "Resep berhasil dihapus"}
        except Exception as e:
            return {"success": False, "message": str(e)}