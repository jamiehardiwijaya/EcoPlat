from business.auth_service import AuthService
from databases.user_repository import UserRepository
from views.dashboard_view import show_dashboard, show_main_app
from utils.helper import Utils

def show_auth_screen():
    Utils.print_header("Food Waste Manager")

def show_auth_menu():
    menu = [
        "🔑 Login",
        "📝 Register",
        "❌ Keluar Aplikasi"
    ]

    print("\nBuat akun atau login untuk mulai mengelola \nmakanan Anda dan mengurangi food waste! 💚")
    
    choice = Utils.pilih_menu(menu)
    
    if choice == 1:
        handle_login()
    elif choice == 2:
        handle_register()
    elif choice == 3:
        print()
        if Utils.confirm_action("Yakin ingin keluar?"):
            print("\n👋 Terima kasih telah menggunakan EcoPlat!")
            exit()
    else:
        Utils.print_error("Pilihan tidak valid!")

def handle_login():
    Utils.print_header("Login")
    print("Ketik 0 pada inputan apa saja untuk kembali ke menu sebelumnya.\n")
   
    while True:
        email    = Utils.get_input   ("Email    :")
        
        if email == "0":
            return
        
        if not email:
            Utils.print_error("Email tidak boleh kosong!\n")
            continue 
            
        if "@" not in email or "." not in email:
            Utils.print_error("Format email tidak valid!")
            print("Contoh format email: abc@gmail.com; xyz@upi.edu\n")
            continue
        
        Utils.loading_animation(0.5, "Memeriksa email")
        email_exists = UserRepository.get_user_by_email(email)
        
        if email_exists:
            Utils.print_success("Email terdaftar!\n")
            break
        else:
            Utils.print_error("Email tidak terdaftar!\n")
            print("Gunakan email yang terdaftar atau \nregister terlebih dahulu.\n")
            continue

    while True:
        password = Utils.get_password("Password :")
        
        if password == "0":
            return
        
        if not password:
            Utils.print_error("Password tidak boleh kosong!\n")
            continue
        
        if len(password) < 6:
            Utils.print_error("Password minimal 6 karakter!\n")
            continue
        
        if not UserRepository.verify_password(email, password):
            Utils.print_error("Password salah!")
            
            while True:
                print("\n=== MENU LUPA PASSWORD ===")
                print("1. Coba lagi")
                print("2. Lupa password")
                print("0. Kembali")
                
                pilih = input("Pilih menu: ").strip()

                if pilih == "1":
                    print()
                    break
                elif pilih == "2":
                    handle_lupa_password(email)
                    return
                elif pilih == "0":
                    return
                else:
                    print()
                    Utils.print_error("Pilihan tidak valid! Silakan masukkan angka \nyang tersedia (1-2) atau 0 untuk kembali.")
                    continue
            continue
        
        Utils.loading_animation(message="Memproses login")
        
        result = AuthService.login_user(email, password)
        break
    
    print()
    if result["success"]:
        Utils.print_success(result["message"])
        Utils.pause_and_clear()
        show_main_app()
    else:
        Utils.print_error(result["message"])
        Utils.pause_and_back()
        handle_login()

def handle_lupa_password(email):
    Utils.print_header("🔑 Lupa Password")

    print(f"Email Anda: {email}")
    print("Ketik 0 pada inputan apa saja untuk kembali ke menu utama.")
    print("\nMasukkan password baru Anda\n")

    while True:
        password = Utils.get_input("Password baru            :")
        if password == "0":
            return
            
        if not password:
            Utils.print_error("Password tidak boleh kosong!\n")
            continue
        
        if len(password) < 6:
            Utils.print_error("Password minimal 6 karakter!\n")
            continue
        break

    while True:
        confirm_password = Utils.get_input ("Konfirmasi password baru :")
        if confirm_password == "0":
            return
            
        if not confirm_password:
            Utils.print_error("Konfirmasi password tidak boleh kosong!\n")
            continue
            
        if password != confirm_password:
            Utils.print_error("Password dan konfirmasi password tidak sesuai!\n")
            continue
        break

    Utils.loading_animation(message="Memproses perubahan password")

    result = AuthService.lupa_password(email, password, confirm_password)

    if result["success"]:
        Utils.print_success(result["message"])
        Utils.pause_and_back("Tekan Enter untuk kembali ke menu utama...")
        return
    else:
        Utils.print_error(result["message"])        

def handle_register(): 
    Utils.print_header("Register")
    print("Ketik 0 pada inputan apa saja untuk kembali ke menu sebelumnya.\n")
    
    # Utils.print_info("Buat akun baru untuk mulai mengelola makanan")
    # print()  # Spacing
    while True:
        nama = Utils.get_input("Nama lengkap\t:")
        
        if nama == "0":
            return
        
        if not nama:
            Utils.print_error("Nama tidak boleh kosong!\n")
            continue
        break
        
    while True:
        email = Utils.get_input("Email \t\t:")
        
        if email == "0":
            return
    
        if not email:
            Utils.print_error("Email tidak boleh kosong!\n")
            continue 
        
        if "@" not in email or "." not in email:
            Utils.print_error("Format email tidak valid!")
            print("Contoh format email: abc@gmail.com; xyz@upi.edu\n")
            continue
        
        Utils.loading_animation(0.5, "Memeriksa email")
        email_exists = UserRepository.get_user_by_email(email)
        
        if email_exists:
            Utils.print_error("Email sudah terdaftar!\n")
            print("Gunakan email lain atau login jika sudah memiliki akun.\n")
            continue
        else:
            Utils.print_success("Email tersedia!\n")
            break
            
    while True:
        password = Utils.get_input("Password (min 6 karakter) :")
        
        if password == "0":
            return
        if not password:
            Utils.print_error("Password tidak boleh kosong!\n")
            continue
        if len(password) < 6:
            Utils.print_error("Password minimal 6 karakter!\n")
            continue
        break
    
    while True:
        confirm_password = Utils.get_input("Konfirmasi password       :")
        
        if confirm_password == "0":
            return
        
        if password != confirm_password:
            Utils.print_error("Password dan konfirmasi password tidak sesuai!\n")
            continue
        break
    
    Utils.loading_animation(message="Memproses registrasi")
     
    result = AuthService.register_user(nama, email, password, confirm_password)
    
    if result["success"]:
        # Utils.wait(1, "Login otomatis")
        
        # # Auto login
        # login_result = AuthService.login_user(email, password)
        # if login_result["success"]:
        Utils.print_success(result["message"])
        Utils.pause_and_clear()
        show_main_app()
    else:
        Utils.print_error(result["message"])
        Utils.pause_and_back()

        
while True:
    show_auth_screen()
    show_auth_menu()