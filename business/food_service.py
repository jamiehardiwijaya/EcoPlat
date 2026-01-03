from databases.makanan_repository import MakananRepository
from business.history_service import HistoryService
from business.recovery_service import RecoveryService
from state import AppState

class FoodService:

    @staticmethod
    def tambah_makanan(nama, jumlah, tanggal_kadaluarsa, kategori):
        user_id = AppState.get_user_id()

        if not user_id:
            return {"success": False, "message": "Anda belum login!"}

        try:
            makanan_id = MakananRepository.tambah_makanan(
                user_id,
                nama.strip(),
                jumlah,
                tanggal_kadaluarsa,
                kategori.strip()
            )

            HistoryService.record_food_addition(
                makanan_id,
                nama.strip(),
                jumlah,
                kategori.strip(),
                tanggal_kadaluarsa
            )

            return {"success": True, "message": "Makanan berhasil ditambahkan!"}

        except Exception as e:
            return {"success": False, "message": "Terjadi kesalahan! Silahkan coba lagi"}

    @staticmethod
    def lihat_makanan():
        user_id = AppState.get_user_id()
        if not user_id:
            return []
        return MakananRepository.get_by_user(user_id)

    @staticmethod
    def hapus_makanan(makanan_id):
        try:
            makanan = MakananRepository.get_by_id(makanan_id)
            if not makanan:
                return {"success": False, "message": "Makanan tidak ditemukan!"}
            
            from datetime import datetime
            today = datetime.now().date()
            
            try:
                exp_date = datetime.strptime(makanan['tanggal_kadaluarsa'], '%Y-%m-%d').date()
                
                if exp_date >= today:
                    alasan = "digunakan"
                    message = "Makanan berhasil dihapus (dicatat sebagai digunakan)!"
                else:
                    alasan = "terbuang"
                    message = "Makanan berhasil dihapus (dicatat sebagai terbuang)!"
                history_result = HistoryService.record_food_deletion(makanan_id, alasan)
                
                if history_result.get("success"):
                    RecoveryService.record_deleted_food(makanan, history_result.get("history_id"), alasan)

                MakananRepository.delete_makanan(makanan_id)
                
                return {"success": True, "message": message}
                    
            except (ValueError, TypeError):
                alasan = "terbuang"
                message = "Makanan berhasil dihapus (dicatat sebagai terbuang)!"
            
            HistoryService.record_food_deletion(makanan_id, alasan)
            MakananRepository.delete_makanan(makanan_id)
            
            return {"success": True, "message": message}
            
        except Exception as e:
            return {"success": False, "message": f"Terjadi kesalahan: {e}"}

    @staticmethod
    def update_makanan(makanan_id, nama, jumlah, tanggal_kadaluarsa, kategori):

        if not nama or not nama.strip():
            return {"success": False, "message": "Nama makanan tidak boleh kosong!"}

        if jumlah is None or str(jumlah).strip() == "":
            return {"success": False, "message": "Jumlah makanan tidak boleh kosong!"}

        try:
            jumlah = int(jumlah)
            if jumlah <= 0:
                return {"success": False, "message": "Jumlah harus lebih dari 0!"}
        except ValueError:
            return {"success": False, "message": "Jumlah harus berupa angka!"}

        if not kategori or not kategori.strip():
            return {"success": False, "message": "Kategori tidak boleh kosong!"}

        try:
            makanan_lama = MakananRepository.get_by_id(makanan_id)

            MakananRepository.update_makanan(
                makanan_id,
                nama.strip(),
                jumlah,
                tanggal_kadaluarsa,
                kategori.strip()
            )

            perubahan = []

            if makanan_lama:
                if makanan_lama["nama_makanan"] != nama:
                    perubahan.append(
                        f"nama: {makanan_lama['nama_makanan']} → {nama}"
                    )

                if str(makanan_lama["jumlah"]) != str(jumlah):
                    perubahan.append(
                        f"jumlah: {makanan_lama['jumlah']} → {jumlah}"
                    )

                if makanan_lama["tanggal_kadaluarsa"] != tanggal_kadaluarsa:
                    perubahan.append(
                        f"tanggal: {makanan_lama['tanggal_kadaluarsa']} → {tanggal_kadaluarsa}"
                    )

                if makanan_lama["kategori"] != kategori:
                    perubahan.append(
                        f"kategori: {makanan_lama['kategori']} → {kategori}"
                    )

            if perubahan:
                HistoryService.record_food_update(
                    makanan_id, ", ".join(perubahan)
                )

            return {"success": True, "message": "Makanan berhasil diupdate!"}
        except Exception as e:
            return {"success": False, "message": f"Terjadi kesalahan: {e}"}