from business.auth_service import AuthService
from views.dashboard_view import show_dashboard, show_main_app

def show_auth_screen():
    print("\n" + "=" * 50)
    print("        🌱 ECOPLAT - Food Waste Manager")
    print("=" * 50)
    
    while True:
        show_auth_menu()

def show_auth_menu():
    print("\n=== MENU AUTH ===")
    print("1. Login")
    print("2. Register")
    print("3. Keluar Aplikasi")
    
    choice = input("Pilih menu [1-3]: ").strip()
    
    if choice == "1":
        handle_login()
    elif choice == "2":
        handle_register()
    elif choice == "3":
        print("Terima kasih telah menggunakan EcoPlat!")
        exit()
    else:
        print("Pilihan tidak valid!")

def handle_login():
    print("\n" + "-" * 30)
    print("LOGIN")
    print("-" * 30)
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    result = AuthService.login_user(email, password)
    
    if result["success"]:
        result["message"]
        input("Tekan Enter untuk melanjutkan...")
        # Pindah ke main app
        show_main_app()
    else:
        result["message"]
        input("Tekan Enter untuk kembali...")

def handle_register():
    print("\n" + "-" * 30)
    print("REGISTER")
    print("-" * 30)
    nama = input("Nama lengkap: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    confirm_password = input("Konfirmasi password: ").strip()
    
    result = AuthService.register_user(nama, email, password, confirm_password)
    
    if result["success"]:
        result["message"]
    else:
        result["message"]
        input("Tekan Enter untuk kembali...")