from state import AppState
from utils.helper import Utils

def show_statistics():
    Utils.print_header("Statistik 📊")
    
    user_id = AppState.get_user_id()
    # Ambil data dari database untuk user ini
    # Contoh:
    # - Total makanan
    # - Makanan hampir kadaluarsa
    # - Makanan sudah kadaluarsa
    # - Total nilai ekonomis
    
    print("Fitur statistik akan tersedia segera...")
    input("\nTekan Enter untuk kembali ke menu utama...")