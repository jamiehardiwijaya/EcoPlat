# views/dashboard_view.py
from state import AppState
from business.auth_service import AuthService
from views.makanan_view import makanan_menu
from views.statistik_view import show_statistics
from utils.helper import Utils
from views.profil_view import show_profil
from views.resep_view import resep_menu

def show_main_app():
    """Menu utama setelah login"""
    while AppState.is_logged_in():
        show_dashboard()

def show_dashboard():
    Utils.print_header("Dashboard Utama")
        
    # List menyimpan teks menu
    menu = [
        "🥦 Kelola Sisa Makanan (Inventaris)",
        "🍲 Kelola Resep",
        "⭐ Rekomendasi Resep",
        "🕘 Riwayat Konsumsi",
        "👤 Profil Saya",
        "🚪 Logout",
        "❌ Keluar Aplikasi"
    ]
    
    Utils.greeting_user()
    
    print("Kelola makanan Anda, selamatkan bumi 💚")

    choice = Utils.pilih_menu(menu)
    
    if choice == "1":
        makanan_menu()
    elif choice == "2":
        resep_menu()
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        show_profil()
    elif choice == "6":
        handle_logout()
    elif choice == 7:
        if Utils.confirm_action("Yakin ingin keluar?"):
            print("\n👋 Terima kasih telah menggunakan EcoPlat!")
            exit()

def handle_logout():
    confirm = input("\nYakin ingin logout? (y/n): ").strip().lower()
    if confirm == 'y':
        result = AuthService.logout_user()
        Utils.print_success(result["message"])
        Utils.pause_and_back("Tekan Enter untuk kembali ke halaman login...")