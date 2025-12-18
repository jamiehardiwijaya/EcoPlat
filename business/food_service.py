from databases.makanan_repository import MakananRepository
from business.history_service import HistoryService  
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
            makanan_id = MakananRepository.tambah_makanan(
                user_id, nama, jumlah, tanggal_kadaluarsa, kategori
            )
            
            history_result = HistoryService.record_food_addition(
                makanan_id, nama, jumlah, kategori, tanggal_kadaluarsa
            )
            
            if not history_result["success"]:
                print(f"⚠️  Peringatan: Gagal mencatat histori: {history_result.get('message', 'Unknown error')}")
            
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
            history_result = HistoryService.record_food_deletion(id)
            
            if not history_result["success"]:
                print(f"⚠️  Peringatan: Gagal mencatat histori penghapusan: {history_result.get('message', 'Unknown error')}")
            
            MakananRepository.delete_makanan(id)
            
            return {"success": True, "message": "Makanan berhasil dihapus!"}
        except Exception as e:
            return {"success": False, "message": f"Terjadi kesalahan: {e}"}
    
    @staticmethod
    def update_makanan(id, nama, jumlah, tanggal_kadaluarsa, kategori):
        """Update makanan dan catat ke histori"""
        try:
            makanan_lama = MakananRepository.get_by_id(id)
            MakananRepository.update_makanan(id, nama, jumlah, tanggal_kadaluarsa, kategori)
            perubahan = []
            if makanan_lama:
                if makanan_lama['nama'] != nama:
                    perubahan.append(f"nama: {makanan_lama['nama']} → {nama}")
                if str(makanan_lama['jumlah']) != str(jumlah):
                    perubahan.append(f"jumlah: {makanan_lama['jumlah']} → {jumlah}")
                if makanan_lama['tanggal_kadaluarsa'] != tanggal_kadaluarsa:
                    perubahan.append(f"tanggal: {makanan_lama['tanggal_kadaluarsa']} → {tanggal_kadaluarsa}")
                if makanan_lama['kategori'] != kategori:
                    perubahan.append(f"kategori: {makanan_lama['kategori']} → {kategori}")
            
            if perubahan:
                history_result = HistoryService.record_food_update(
                    id, ", ".join(perubahan)
                )
                if not history_result["success"]:
                    print(f"⚠️  Peringatan: Gagal mencatat histori update: {history_result.get('message', 'Unknown error')}")
            
            return {"success": True, "message": "Makanan berhasil diupdate!"}
        except Exception as e:
            return {"success": False, "message": f"Terjadi kesalahan: {e}"}