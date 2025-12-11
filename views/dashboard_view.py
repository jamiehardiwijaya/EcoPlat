# views/dashboard_view.py
from state import AppState
from views.makanan_view import makanan_menu
# from views.resep_view import show_resep_menu
# from views.profil_view import show_profil

def show_main_app():
    """Menu utama setelah login"""
    while AppState.is_logged_in():
        show_dashboard()

def show_dashboard():
    user_name = AppState.get_user_name()
    
    print("\n" + "=" * 50)
    print(f"    ECOPLAT - Dashboard")
    print(f"    User: {user_name}")
    print("=" * 50)
    
    print("\n=== MENU UTAMA ===")
    print("1. 📊 Dashboard & Statistik")
    print("2. 🥦 Kelola Makanan (Inventaris)")
    print("3. 📋 Lihat Resep & Rekomendasi")
    print("4. 👤 Profil Saya")
    print("5. 🚪 Logout")
    
    choice = input("\nPilih menu [1-5]: ").strip()
    
    if choice == "1":
        show_statistics()
    elif choice == "2":
        makanan_menu()
        pass
    elif choice == "3":
        # show_resep_menu()
        pass
    elif choice == "4":
        # show_profil()
        pass
    elif choice == "5":
        handle_logout()
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