from databases.makanan_repository import MakananRepository
from business.history_service import HistoryService
from state import AppState
from datetime import datetime, timedelta

class ExpirationService:
    
    @staticmethod
    def check_expired_foods(record_to_history=True):
        """Memeriksa dan menandai makanan yang sudah kadaluarsa"""
        user_id = AppState.get_user_id()
        if not user_id:
            return []
            
        makanan_list = MakananRepository.get_by_user(user_id)
        
        expired_foods = []
        today = datetime.now().date()
        
        for makanan in makanan_list:
            try:
                if not makanan.get('tanggal_kadaluarsa'):
                    continue
                    
                exp_date = datetime.strptime(makanan['tanggal_kadaluarsa'], '%Y-%m-%d').date()
                
                if exp_date < today:
                    if record_to_history:
                        HistoryService.record_food_deletion(makanan['id'], "terbuang")
                    
                    expired_foods.append({
                        'id': makanan['id'],
                        'nama': makanan['nama_makanan'],
                        'jumlah': makanan['jumlah'],
                        'tanggal_kadaluarsa': makanan['tanggal_kadaluarsa'],
                        'hari_terlambat': (today - exp_date).days
                    })
                    
            except (ValueError, TypeError):
                continue
        
        return expired_foods
    
    @staticmethod
    def get_almost_expired_foods(days_threshold=3):
        """Mendapatkan makanan yang hampir kadaluarsa"""
        user_id = AppState.get_user_id()
        if not user_id:
            return []
        
        makanan_list = MakananRepository.get_by_user(user_id)
        
        almost_expired = []
        today = datetime.now().date()
        
        for makanan in makanan_list:
            try:
                if not makanan.get('tanggal_kadaluarsa'):
                    continue
                    
                exp_date = datetime.strptime(makanan['tanggal_kadaluarsa'], '%Y-%m-%d').date()
                
                days_left = (exp_date - today).days
                if 0 <= days_left <= days_threshold:
                    almost_expired.append({
                        'id': makanan['id'],
                        'nama': makanan['nama_makanan'],
                        'jumlah': makanan['jumlah'],
                        'tanggal_kadaluarsa': makanan['tanggal_kadaluarsa'],
                        'hari_tersisa': days_left
                    })
                    
            except (ValueError, TypeError):
                continue
        
        return almost_expired