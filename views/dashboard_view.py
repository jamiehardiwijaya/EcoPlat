from state import AppState
from business.auth_service import AuthService
from views.makanan_view import makanan_menu
from views.statistik_view import show_statistics
from utils.helper import Utils
from views.profil_view import show_profil
from views.resep_view import resep_menu
from views.history_view import history_menu

_notification_shown = False

def show_main_app():
    """Menu utama setelah login"""
    global _notification_shown
    _notification_shown = False
    
    while AppState.is_logged_in():
        show_dashboard()
    
    _notification_shown = False
    Utils.clear_screen()
    from views.auth_view import show_auth_menu
    show_auth_menu()

def show_dashboard():
    """Menampilkan dashboard dengan notifikasi hanya sekali"""
    global _notification_shown
    
    if not _notification_shown:
        show_expiration_notifications_once()
        _notification_shown = True
    
    Utils.print_header("Dashboard Utama")
    
    menu = [
        "🥦 Kelola Sisa Makanan (Inventaris)",
        "🍲 Kelola Resep",
        "⭐ Rekomendasi Resep",
        "📜 Histori Aktivitas",
        "👤 Profil Saya",
        "🚪 Logout",
        "❌ Keluar Aplikasi"
    ]
    
    Utils.greeting_user()
    
    print("Kelola makanan Anda, selamatkan bumi 💚")

    choice = Utils.pilih_menu(menu)
    
    if choice == 1:
        makanan_menu()
    elif choice == 2:
        resep_menu()
    elif choice == 3:
        show_rekomendasi_menu()
    elif choice == 4:
        history_menu()
    elif choice == 5:
        show_profil()
    elif choice == 6:
        if handle_logout():
            return 
    elif choice == 7:
        if Utils.confirm_action("Yakin ingin keluar?"):
            print("\n👋 Terima kasih telah menggunakan EcoPlat!")
            exit()

def show_expiration_notifications_once():
    """Tampilkan notifikasi makanan kadaluarsa HANYA SEKALI saat login pertama"""
    try:
        from databases.makanan_repository import MakananRepository
        from datetime import datetime
        
        user_id = AppState.get_user_id()
        if not user_id:
            return
        
        semua_makanan = MakananRepository.get_by_user(user_id)
        if not semua_makanan:
            return
        
        today = datetime.now()
        makanan_kadaluarsa = []
        makanan_hampir_kadaluarsa = []
        
        for makanan in semua_makanan:
            tanggal_str = makanan.get('tanggal_kadaluarsa')
            if not tanggal_str:
                continue
                
            try:
                exp_date = datetime.strptime(tanggal_str, '%Y-%m-%d')
                hari = (exp_date - today).days
                
                if hari < 0:
                    makanan_kadaluarsa.append({
                        'nama': makanan['nama_makanan'],
                        'jumlah': makanan['jumlah'],
                        'kategori': makanan['kategori'],
                        'tanggal': tanggal_str,
                        'hari_lewat': abs(hari)
                    })
                elif 0 <= hari <= 3:
                    makanan_hampir_kadaluarsa.append({
                        'nama': makanan['nama_makanan'],
                        'jumlah': makanan['jumlah'],
                        'kategori': makanan['kategori'],
                        'tanggal': tanggal_str,
                        'hari_tersisa': hari
                    })
                    
            except ValueError:
                continue
        
        if makanan_kadaluarsa or makanan_hampir_kadaluarsa:
            Utils.clear_screen()
            print("=" * 60)
            print("      🔔 NOTIFIKASI AWAL LOGIN 🔔")
            print("=" * 60)
            print(f"📅 Selamat datang kembali! Berikut status makanan Anda:\n")
            
            if makanan_kadaluarsa:
                print("❌ MAKANAN SUDAH KADALUARSA:")
                print("-" * 40)
                for makanan in makanan_kadaluarsa:
                    hari_text = "hari ini" if makanan['hari_lewat'] == 0 else f"{makanan['hari_lewat']} hari lalu"
                    print(f"• {makanan['nama']} ({makanan['jumlah']} {makanan['kategori']})")
                    print(f"  Kadaluarsa: {makanan['tanggal']} ({hari_text})")
                    print()
            
            if makanan_hampir_kadaluarsa:
                print("⚠️  MAKANAN HAMPIR KADALUARSA:")
                print("-" * 40)
                for makanan in makanan_hampir_kadaluarsa:
                    if makanan['hari_tersisa'] == 0:
                        hari_text = "HARI INI!"
                    elif makanan['hari_tersisa'] == 1:
                        hari_text = "BESOK!"
                    else:
                        hari_text = f"{makanan['hari_tersisa']} hari lagi"
                    
                    print(f"• {makanan['nama']} ({makanan['jumlah']} {makanan['kategori']})")
                    print(f"  Kadaluarsa: {makanan['tanggal']} → {hari_text}")
                    print()
            
            print("=" * 60)
            print("\n💡 Informasi ini hanya ditampilkan sekali saat login.")
            print("   Untuk update terkini, cek menu '🥦 Kelola Makanan'.")
            
            print("\n" + "=" * 60)
            input("\nTekan Enter untuk melanjutkan ke Dashboard... ")
            Utils.clear_screen()
            
    except Exception as e:

        print(f"⚠️  Error notifikasi: {str(e)[:50]}")

def handle_logout():
    confirm = input("\nYakin ingin logout? (y/n): ").strip().lower()
    if confirm == 'y':
        result = AuthService.logout_user()
        Utils.print_success(result["message"])
        Utils.pause_and_clear()
        return True  
    return False

def show_rekomendasi_menu():
    Utils.print_header("⭐ Rekomendasi Resep")
    print("Fitur rekomendasi resep sedang dalam pengembangan...")
    print("Akan segera hadir dengan AI-powered recommendations!")
    Utils.pause_and_back()