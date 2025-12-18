from databases.history_repository import HistoryRepository
from databases.makanan_repository import MakananRepository
from state import AppState
from datetime import datetime, timedelta

class HistoryService:
    
    @staticmethod
    def record_food_addition(makanan_id, nama, jumlah, kategori, tanggal_kadaluarsa):
        """Mencatat penambahan makanan ke histori"""
        user_id = AppState.get_user_id()
        if not user_id:
            return {"success": False, "message": "User tidak login"}
        
        try:
            HistoryRepository.tambah_history(
                user_id=user_id,
                sisa_makanan_id=makanan_id,
                tanggal_kadaluwarsa=tanggal_kadaluarsa,
                jenis_makanan=kategori,
                jumlah=jumlah,
                status="ditambahkan",
                nama=nama
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": f"Gagal mencatat histori: {e}"}
    
    @staticmethod
    def record_food_deletion(makanan_id, alasan="dihapus"):
        """Mencatat penghapusan makanan ke histori"""
        user_id = AppState.get_user_id()
        if not user_id:
            return {"success": False, "message": "User tidak login"}
        
        makanan = MakananRepository.get_by_id(makanan_id)
        if not makanan:
            return {"success": False, "message": "Makanan tidak ditemukan"}
        
        try:
            HistoryRepository.tambah_history(
                user_id=user_id,
                sisa_makanan_id=makanan_id,
                tanggal_kadaluwarsa=makanan['tanggal_kadaluarsa'],
                jenis_makanan=makanan['kategori'],
                jumlah=makanan['jumlah'],
                status=alasan,
                nama=makanan['nama_makanan']
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": f"Gagal mencatat histori: {e}"}
    
    @staticmethod
    def record_food_expired(makanan_id):
        """Mencatat makanan kadaluarsa ke histori"""
        return HistoryService.record_food_deletion(makanan_id, "kadaluarsa")
    
    @staticmethod
    def record_food_used(makanan_id):
        """Mencatat makanan digunakan/dimasak ke histori"""
        return HistoryService.record_food_deletion(makanan_id, "digunakan")
    
    @staticmethod
    def record_food_consumed(makanan_id):
        """Mencatat makanan dikonsumsi ke histori"""
        return HistoryService.record_food_deletion(makanan_id, "dikonsumsi")
    
    @staticmethod
    def record_food_update(makanan_id, perubahan):
        """Mencatat perubahan/update makanan"""
        user_id = AppState.get_user_id()
        if not user_id:
            return {"success": False, "message": "User tidak login"}
        
        makanan = MakananRepository.get_by_id(makanan_id)
        if not makanan:
            return {"success": False, "message": "Makanan tidak ditemukan"}
        
        try:
            HistoryRepository.tambah_history(
                user_id=user_id,
                sisa_makanan_id=makanan_id,
                tanggal_kadaluwarsa=makanan['tanggal_kadaluarsa'],
                jenis_makanan=makanan['kategori'],
                jumlah=makanan['jumlah'],
                status=f"diupdate ({perubahan})",
                nama=makanan['nama_makanan']
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": f"Gagal mencatat histori: {e}"}
    
    @staticmethod
    def lihat_histori(limit=None):
        """Melihat histori aktivitas"""
        user_id = AppState.get_user_id()
        if not user_id:
            return []
        
        if limit:
            return HistoryRepository.get_history_by_user(user_id, limit)
        return HistoryRepository.get_history_by_user(user_id)
    
    @staticmethod
    def lihat_histori_periode(start_date, end_date):
        """Melihat histori berdasarkan periode"""
        user_id = AppState.get_user_id()
        if not user_id:
            return []
        
        return HistoryRepository.get_history_by_date_range(user_id, start_date, end_date)
    
    @staticmethod
    def get_statistik_histori():
        """Mendapatkan statistik histori"""
        user_id = AppState.get_user_id()
        if not user_id:
            return {}
        
        stats = HistoryRepository.get_history_statistics(user_id)
        
        result = {
            "total_aktivitas": 0,
            "total_item": 0,
            "detail": {},
            "ringkasan": {},
            "analisis": {}
        }
        
        total_aktivitas = 0
        total_item = 0
        
        for stat in stats:
            status = stat['status']
            jenis = stat['jenis_makanan'] or 'lainnya'
            
            if status not in result["detail"]:
                result["detail"][status] = {
                    "jumlah_aktivitas": 0,
                    "total_item": 0,
                    "by_category": {}
                }
            
            result["detail"][status]["jumlah_aktivitas"] += stat['total_aktivitas']
            result["detail"][status]["total_item"] += stat['total_item']
            
            if jenis not in result["detail"][status]["by_category"]:
                result["detail"][status]["by_category"][jenis] = 0
            result["detail"][status]["by_category"][jenis] += stat['total_item']
            
            total_aktivitas += stat['total_aktivitas']
            total_item += stat['total_item']
        
        result["total_aktivitas"] = total_aktivitas
        result["total_item"] = total_item
        
        recent = HistoryRepository.get_recent_activities(user_id, 5)
        result["ringkasan"]["terbaru"] = recent
        
        today = HistoryRepository.get_today_history(user_id)
        yesterday = HistoryRepository.get_yesterday_history(user_id)
        result["ringkasan"]["hari_ini"] = len(today)
        result["ringkasan"]["kemarin"] = len(yesterday)
        
        wasted_food = HistoryRepository.get_wasted_food_history(user_id)
        used_food = HistoryRepository.get_food_usage_history(user_id)
        
        result["analisis"]["total_terbuang"] = len(wasted_food)
        result["analisis"]["total_digunakan"] = len(used_food)
        
        if total_aktivitas > 0:
            result["analisis"]["persentase_terbuang"] = (len(wasted_food) / total_aktivitas) * 100
            result["analisis"]["persentase_digunakan"] = (len(used_food) / total_aktivitas) * 100
        
        return result
    
    @staticmethod
    def get_wasted_food_report():
        """Mendapatkan laporan makanan terbuang"""
        user_id = AppState.get_user_id()
        if not user_id:
            return []
        
        return HistoryRepository.get_wasted_food_history(user_id)
    
    @staticmethod
    def get_monthly_summary(year_month=None):
        """Mendapatkan ringkasan bulanan"""
        user_id = AppState.get_user_id()
        if not user_id:
            return {}
        
        if not year_month:
            year_month = datetime.now().strftime('%Y-%m')
        
        return HistoryRepository.get_monthly_summary(user_id, year_month)
    
    @staticmethod
    def search_history(keyword):
        """Mencari histori berdasarkan keyword"""
        user_id = AppState.get_user_id()
        if not user_id:
            return []
        
        return HistoryRepository.search_history(user_id, keyword)