from databases.makanan_repository import MakananRepository
from state import AppState

class FoodService:

    @staticmethod
    def tambah_makanan(nama, jumlah, tanggal_kadaluarsa, kategori):
        user_id = AppState.get_user_id()

        if not user_id:
            return {"success": False, "message": "Anda belum login!"}
        
        if not nama or not jumlah:
            return {"success": False, "message": "Nama dan jumlah makanan harus diisi!"}
        
        try:
            MakananRepository.tambah_makanan(user_id ,nama, jumlah, tanggal_kadaluarsa, kategori)
            return {"success": True, "message": "Makanan berhasil ditambahkan!"}
        except Exception as e:
            return {"success": False, "message": f"Terjadi kesalahan: {e}"}
        
    @staticmethod
    def lihat_makanan():
        user = AppState.get_user_id()
        if not user:
            return []
        return MakananRepository.get_by_user(user)
    
    @staticmethod
    def hapus_makanan(id):
        try:
            MakananRepository.delete_makanan(id)
            return {"success": True, "message": "Makanan berhasil dihapus!"}
        except Exception as e:
            return {"success": False, "message": f"Terjadi kesalahan: {e}"}