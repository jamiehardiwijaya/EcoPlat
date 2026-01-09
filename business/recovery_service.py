import pandas as pd
import os
from datetime import datetime
from databases.makanan_repository import MakananRepository
from databases.history_repository import HistoryRepository
from business.history_service import HistoryService
from state import AppState
from utils.helper import Utils

class RecoveryService:
    CSV_PATH = "deleted_foods.csv"
    
    @staticmethod
    def _ensure_csv_exists():
        """Memastikan file CSV ada dengan header yang benar"""
        if not os.path.exists(RecoveryService.CSV_PATH):
            df = pd.DataFrame(columns=[
                'id', 'user_id', 'nama_makanan', 'jumlah', 
                'kategori', 'tanggal_kadaluarsa', 'deleted_at',
                'original_history_id', 'status_deletion', 'is_recovered',
                'recovered_at'
            ])
            df.to_csv(RecoveryService.CSV_PATH, index=False)
    
    @staticmethod
    def record_deleted_food(makanan, history_id, status_deletion="dihapus"):
        try:
            RecoveryService._ensure_csv_exists()
            
            user_id = AppState.get_user_id()
            
            deleted_record = {
                'id': makanan['id'],
                'user_id': user_id,
                'nama_makanan': makanan['nama_makanan'],
                'jumlah': makanan['jumlah'],
                'kategori': makanan['kategori'],
                'tanggal_kadaluarsa': makanan['tanggal_kadaluarsa'],
                'deleted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'original_history_id': history_id,
                'status_deletion': status_deletion,
                'is_recovered': 0, 
                'recovered_at': None
            }
            
            df = pd.read_csv(RecoveryService.CSV_PATH)
            df = Utils._normalize_types(df)
            

            existing_mask = (df['id'] == makanan['id']) & (df['is_recovered'] == 0) & (df['user_id'] == user_id)
            if existing_mask.any():
                for col, value in deleted_record.items():
                    df.loc[existing_mask, col] = value
            else:
                new_df = pd.DataFrame([deleted_record])
                df = pd.concat([df, new_df], ignore_index=True)
            
            df.to_csv(RecoveryService.CSV_PATH, index=False)
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def get_deleted_foods(user_id=None):
        try:
            RecoveryService._ensure_csv_exists()
            
            df = pd.read_csv(RecoveryService.CSV_PATH)
            df = Utils._normalize_types(df)
            
            if df.empty:
                return []
            
            if user_id:
                df = df[(df['user_id'] == user_id) & (df['is_recovered'] == 0)]
            else:
                df = df[df['is_recovered'] == 0]

            deleted_foods = df.to_dict('records')
            
            for food in deleted_foods:
                food['id'] = int(food['id'])
                food['user_id'] = int(food['user_id'])
                food['jumlah'] = int(food['jumlah'])
            
            return deleted_foods
            
        except Exception:
            return []
    
    @staticmethod
    def recover_food(deleted_food_id):
        try:
            RecoveryService._ensure_csv_exists()
            
            df = pd.read_csv(RecoveryService.CSV_PATH)
            df = Utils._normalize_types(df)
 
            mask = (df['id'] == deleted_food_id) & (df['is_recovered'] == 0)
            
            if not mask.any():
                return {"success": False, "message": "Makanan tidak ditemukan atau sudah dipulihkan"}
            
            food_row = df[mask].iloc[0]
            food_data = food_row.to_dict()
            
            user_id = int(food_data['user_id'])
            current_user_id = AppState.get_user_id()

            if user_id != current_user_id:
                return {"success": False, "message": "Anda tidak memiliki izin untuk memulihkan makanan ini"}
            
            new_food_id = MakananRepository.tambah_makanan(
                user_id,
                food_data['nama_makanan'],
                int(food_data['jumlah']),
                food_data['tanggal_kadaluarsa'],
                food_data['kategori']
            )
            
            history_id = HistoryRepository.tambah_history(
                user_id=user_id,
                sisa_makanan_id=new_food_id,
                tanggal_kadaluwarsa=food_data['tanggal_kadaluarsa'],
                jenis_makanan=food_data['kategori'],
                jumlah=int(food_data['jumlah']),
                status="dipulihkan",
                nama=food_data['nama_makanan']
            )
            
            try:
                from databases.db import execute_query
                execute_query(
                    "UPDATE user_history SET status = 'dibatalkan' WHERE id = ?",
                    (int(food_data['original_history_id']),)
                )
            except Exception:
                pass  

            df.loc[mask, 'is_recovered'] = 1
            df.loc[mask, 'recovered_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            df.to_csv(RecoveryService.CSV_PATH, index=False)
            
            return {
                "success": True, 
                "message": f"✅ Makanan '{food_data['nama_makanan']}' berhasil dipulihkan!",
                "new_food_id": new_food_id
            }
            
        except Exception as e:
            return {"success": False, "message": f"❌ Gagal memulihkan makanan: {str(e)}"}
    
    @staticmethod
    def permanently_delete_from_csv(deleted_food_id):
        try:
            RecoveryService._ensure_csv_exists()
            
            df = pd.read_csv(RecoveryService.CSV_PATH)
            df = Utils._normalize_types(df)
            
            initial_count = len(df)
            df = df[df['id'] != deleted_food_id]
            final_count = len(df)
            
            df.to_csv(RecoveryService.CSV_PATH, index=False)
            
            deleted_count = initial_count - final_count
            return {"success": True, "message": f"🗑️ Record berhasil dihapus permanen", "deleted_count": deleted_count}
            
        except Exception as e:
            return {"success": False, "message": f"❌ Error: {str(e)}"}
    
    @staticmethod
    def cleanup_old_records(days=30):
        try:
            RecoveryService._ensure_csv_exists()
            
            df = pd.read_csv(RecoveryService.CSV_PATH)
            df = Utils._normalize_types(df)
            
            if df.empty:
                return {"success": True, "deleted_count": 0}

            df['deleted_at_dt'] = pd.to_datetime(df['deleted_at'], errors='coerce')
            
            current_time = datetime.now()
            df['days_ago'] = (current_time - df['deleted_at_dt']).dt.days

            old_mask = (df['days_ago'] > days) & (df['is_recovered'] == 1)
            deleted_count = old_mask.sum()
            
            df = df[~old_mask]
            
            df = df.drop(columns=['deleted_at_dt', 'days_ago'], errors='ignore')
            
            df.to_csv(RecoveryService.CSV_PATH, index=False)
            
            return {"success": True, "deleted_count": int(deleted_count)}
            
        except Exception as e:
            return {"success": False, "message": f"❌ Error: {str(e)}"}
    
    @staticmethod
    def get_waste_reduction_stats():
        try:
            RecoveryService._ensure_csv_exists()
            
            df = pd.read_csv(RecoveryService.CSV_PATH)
            df = Utils._normalize_types(df)
            
            if df.empty:
                return {
                    "total_deleted": 0,
                    "total_recovered": 0,
                    "recovery_rate": 0,
                    "waste_prevented": 0
                }
            
            user_id = AppState.get_user_id()
            user_df = df[df['user_id'] == user_id]
            
            total_deleted = len(user_df)
            total_recovered = len(user_df[user_df['is_recovered'] == 1])
            
            if total_deleted > 0:
                recovery_rate = (total_recovered / total_deleted) * 100
            else:
                recovery_rate = 0
            
            waste_prevented = user_df[user_df['is_recovered'] == 1]['jumlah'].sum() if total_recovered > 0 else 0
            
            return {
                "total_deleted": int(total_deleted),
                "total_recovered": int(total_recovered),
                "recovery_rate": float(recovery_rate),
                "waste_prevented": int(waste_prevented)
            }
            
        except Exception:
            return {
                "total_deleted": 0,
                "total_recovered": 0,
                "recovery_rate": 0,
                "waste_prevented": 0
            }