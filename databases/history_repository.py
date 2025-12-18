from databases.db import execute_query, fetch_all, fetch_one
from datetime import datetime, timedelta

class HistoryRepository:
    
    @staticmethod
    def tambah_history(user_id, sisa_makanan_id, tanggal_kadaluwarsa, 
                      jenis_makanan, jumlah, status, nama):
        query = """
            INSERT INTO user_history 
            (user_id, sisa_makanan_id, tanggal_kadaluwarsa, jenis_makanan, jumlah, status, nama)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return execute_query(query, (
            user_id, sisa_makanan_id, tanggal_kadaluwarsa, 
            jenis_makanan, jumlah, status, nama
        ))
    
    @staticmethod
    def get_history_by_user(user_id, limit=None):
        query = """
            SELECT 
                uh.*,
                sm.nama_makanan as nama_makanan_asli,
                sm.kategori as kategori_asli
            FROM user_history uh
            LEFT JOIN sisa_makanan sm ON uh.sisa_makanan_id = sm.id
            WHERE uh.user_id = ? 
            ORDER BY uh.timestamp DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def get_history_by_date_range(user_id, start_date, end_date):
        query = """
            SELECT 
                uh.*,
                sm.nama_makanan as nama_makanan_asli,
                sm.kategori as kategori_asli
            FROM user_history uh
            LEFT JOIN sisa_makanan sm ON uh.sisa_makanan_id = sm.id
            WHERE uh.user_id = ? 
            AND DATE(uh.timestamp) BETWEEN ? AND ?
            ORDER BY uh.timestamp DESC
        """
        return fetch_all(query, (user_id, start_date, end_date))
    
    @staticmethod
    def get_history_statistics(user_id):
        query = """
            SELECT 
                status,
                COUNT(*) as total_aktivitas,
                SUM(jumlah) as total_item,
                jenis_makanan
            FROM user_history 
            WHERE user_id = ?
            GROUP BY status, jenis_makanan
        """
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def get_recent_activities(user_id, limit=5):
        query = """
            SELECT * FROM user_history 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        return fetch_all(query, (user_id, limit))
    
    @staticmethod
    def get_today_history(user_id):
        """Mendapatkan histori hari ini"""
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT * FROM user_history 
            WHERE user_id = ? 
            AND DATE(timestamp) = ?
            ORDER BY timestamp DESC
        """
        return fetch_all(query, (user_id, today))
    
    @staticmethod
    def get_yesterday_history(user_id):
        """Mendapatkan histori kemarin"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        query = """
            SELECT * FROM user_history 
            WHERE user_id = ? 
            AND DATE(timestamp) = ?
            ORDER BY timestamp DESC
        """
        return fetch_all(query, (user_id, yesterday))
    
    @staticmethod
    def get_history_by_status(user_id, status):
        """Mendapatkan histori berdasarkan status tertentu"""
        query = """
            SELECT * FROM user_history 
            WHERE user_id = ? AND status = ?
            ORDER BY timestamp DESC
        """
        return fetch_all(query, (user_id, status))
    
    @staticmethod
    def get_wasted_food_history(user_id):
        """Mendapatkan histori makanan yang terbuang"""
        return HistoryRepository.get_history_by_status(user_id, "kadaluarsa")
    
    @staticmethod
    def get_food_usage_history(user_id):
        """Mendapatkan histori makanan yang digunakan"""
        query = """
            SELECT * FROM user_history 
            WHERE user_id = ? AND (status = 'digunakan' OR status = 'dikonsumsi')
            ORDER BY timestamp DESC
        """
        return fetch_all(query, (user_id,))
    
    @staticmethod
    def get_monthly_summary(user_id, year_month):
        """Mendapatkan ringkasan bulanan"""
        query = """
            SELECT 
                DATE(timestamp) as tanggal,
                status,
                COUNT(*) as jumlah_aktivitas,
                SUM(jumlah) as total_item
            FROM user_history 
            WHERE user_id = ? 
            AND strftime('%Y-%m', timestamp) = ?
            GROUP BY DATE(timestamp), status
            ORDER BY tanggal DESC
        """
        return fetch_all(query, (user_id, year_month))
    
    @staticmethod
    def search_history(user_id, keyword):
        """Mencari histori berdasarkan keyword"""
        query = """
            SELECT * FROM user_history 
            WHERE user_id = ? 
            AND (nama LIKE ? OR jenis_makanan LIKE ? OR status LIKE ?)
            ORDER BY timestamp DESC
        """
        search_term = f"%{keyword}%"
        return fetch_all(query, (user_id, search_term, search_term, search_term))