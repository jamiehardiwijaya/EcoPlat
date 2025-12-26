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

            for nama_bahan_input in daftar_bahan:
                nama_normal = nama_bahan_input.strip().lower()
                
                if not nama_normal:
                    continue

                bahan = BahanRepository.get_by_name_case_insensitive(nama_normal)

                if bahan:
                    bahan_id = bahan["id"]
                else:
                    nama_simpan = nama_normal.capitalize()
                    bahan_id = BahanRepository.tambah_bahan(nama_simpan)

                BahanResepRepository.tambah(resep_id, bahan_id)

            return {"success": True, "message": "Resep & bahan berhasil disimpan"}

        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def lihat_resep_saya():
        user_id = AppState.get_user_id()
        resep_list = ResepRepository.get_by_user(user_id)
    
        for resep in resep_list:
            bahan = BahanResepRepository.get_bahan_by_resep(resep["id"])
            resep["bahan"] = [b["nama"] for b in bahan]

        return resep_list

    @staticmethod
    def lihat_semua_resep():
        resep_list = ResepRepository.get_all()
    
        for resep in resep_list:
            bahan = BahanResepRepository.get_bahan_by_resep(resep["id"])
            resep["bahan"] = [b["nama"] for b in bahan]

        return resep_list

    @staticmethod
    def hapus_resep(resep_id):
        user_id = AppState.get_user_id()

        try:
            ResepRepository.delete_resep(resep_id, user_id)
            return {"success": True, "message": "Resep berhasil dihapus"}
        except Exception as e:
            return {"success": False, "message": str(e)}