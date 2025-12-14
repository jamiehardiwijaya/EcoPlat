# views/dashboard_view.py
from state import AppState
from views.makanan_view import makanan_menu
from views.resep_view import resep_menu
# from views.rekomendasi_view import tampilkan_rekomendasi
# from views.profil_view import show_profil

from utils.helper import Utils

def show_main_app():
    """Menu utama setelah logibn"""
    while AppState.is_logged_in():
        show_dashboard()

def show_dashboard():
    user_name = AppState.get_user_name()
    
    print("\n" + "=" * 50)
    print(f"    ECOPLAT - Dashboard")
    print(f"    User: {user_name}")
    print("=" * 50)
    
    print("\n=== MENU UTAMA ===")
<<<<<<< HEAD
    print("1. 🥦 Kelola Makanan (Inventaris)")
    print("2. 📋 Kelola Resep")
    print("3. ⭐ Rekomendasi Resep")
    print("4. 🕘 Riwayat Konsumsi")
    print("5. 👤 Profil Saya")
    print("6. 🚪 Logout")
=======
    print("1. 📊 Dashboard & Statistik")
    print("2. 🥦 Kelola Makanan (Inventaris)")
    print("3. 📋 Lihat Resep & Rekomendasi")
    print("4. 👤 Profil Saya")
    print("5. 🚪 Logout")
    print("6. Keluar")
>>>>>>> 2d98fb5 (fix: stylishing authentication view)
    
    choice = input("\nPilih menu [1-6]: ").strip()
    
    if choice == "1":
        makanan_menu()
    elif choice == "2":
        resep_menu()
    elif choice == "3":
        # tampilkan_rekomendasi()
        pass
    elif choice == "4":
        # show_riwayat_konsumsi()
        pass
    elif choice == "5":
        # show_profil()
        pass
    elif choice == "6":
        handle_logout()
    elif choice == "6":
        if Utils.confirm_action("Yakin ingin keluar?"):
            print("\n👋 Terima kasih telah menggunakan EcoPlat!")
            exit()
    else:
        print("Pilihan tidak valid!")

def show_statistics():
    print("\n" + "=" * 30)
    print("    DASHBOARD STATISTIK")
    print("=" * 30)
    
    user_id = AppState.get_user_id()
    # Ambil data dari database untuk user ini
    # Contoh:
    # - Total makanan
    # - Makanan hampir kadaluarsa
    # - Makanan sudah kadaluarsa
    # - Total nilai ekonomis
    
    print("Fitur statistik akan tersedia segera...")
    input("\nTekan Enter untuk kembali ke menu utama...")

def handle_logout():
    confirm = input("\nYakin ingin logout? (y/n): ").strip().lower()
    if confirm == 'y':
        AppState.logout()
        print("✓ Anda telah logout.")
        input("Tekan Enter untuk kembali ke halaman login...")