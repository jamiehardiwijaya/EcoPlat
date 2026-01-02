from state import AppState
from utils.helper import Utils
from business.auth_service import AuthService
from databases.user_repository import UserRepository

def show_profil():
    Utils.print_header("Profil Saya", show_user=False)
    
    current_nama = AppState.get_user_name()
    current_email = AppState.get_user_email()
    
    print("Profil Anda\n")
    print(f"Nama  : {current_nama or 'N/A'}")
    print(f"Email : {current_email or 'N/A'}")
    print("\nApa yang ingin Anda lakukan?")

    menu = [
        "📝 Ubah Nama", 
        "📧 Ubah Email",
        "🔒 Ubah Password",
        "🏠 Kembali ke Dashboard"
    ]
    
    choice = Utils.pilih_menu(menu)
    
    if choice == 1:
        ubah_nama()
    elif choice == 2:
        ubah_email()
        pass
    elif choice == 3:
        ubah_password()
        pass
    elif choice == 4:
        return
    
    show_profil()
    
# Utils.pause_and_back("Tekan Enter untuk kembali ke dashboard utama...")

def ubah_nama():
    def render_header():
        Utils.print_header("Ubah Nama", show_user=False)
        print("Ketik 0 untuk batal dan kembali ke menu profil.\n")
        print(f"Nama Anda saat ini: {AppState.get_user_name() or 'N/A'}\n")

    # tampilkan header sekali di awal
    render_header()
    
    user_id = AppState.get_user_id()
    if not user_id:
        Utils.print_error("ID user tidak valid! Menu ini dilarang diakses.")
        Utils.pause_and_back("Tekan Enter untuk kembali ke menu profil...")
        return
    
    while True:  # loop utama untuk form ubah nama
        nama = Utils.get_input("Nama baru         :")
        
        if nama == "0":
            return
        
        if not nama:
            Utils.print_error("Nama tidak boleh kosong!\n")
            continue 
        
        # konfirmasi
        if Utils.confirm_action(f"Yakin ingin memperbarui nama Anda ({nama})?"):
            Utils.loading_animation(message="Memperbarui nama")
            result = AuthService.update_user_name(user_id, nama)

            if result["success"]:
                Utils.print_success(result["message"])
                AppState.set_user_name(nama)
                Utils.pause_and_back("Tekan Enter untuk kembali ke menu profil...")
                return
            else:
                Utils.print_error(result["message"])
                continue
        else:
            Utils.clear_screen()
            render_header()
            print("Perubahan dibatalkan. Silakan masukkan nama baru lagi \natau 0 untuk batal.\n")
            continue

def ubah_email():
    def render_header():
        Utils.print_header("Ubah Email", show_user=False)
        print("Ketik 0 untuk batal dan kembali ke menu profil.\n")
        print(f"Email Anda saat ini: {AppState.get_user_email() or 'N/A'}\n")
    # tampilkan header sekali di awal
    render_header()
    
    user_id = AppState.get_user_id()
    if not user_id:
        Utils.print_error("ID user tidak valid! Menu ini dilarang diakses.")
        Utils.pause_and_back("Tekan Enter untuk kembali ke menu profil...")
        return  
    
    while True:  # loop utama untuk form ubah email
        email = Utils.get_input("Email baru         :")
        
        if email == "0":
            return
        
        if not email:
            Utils.print_error("Email tidak boleh kosong!\n")
            continue
        
        if "@" not in email or "." not in email:
            Utils.print_error("Format email tidak valid!")
            print("Contoh format email: abc@gmail.com; xyz@upi.edu\n")
            continue
        
        if email == AppState.get_user_email():
        # if email == "jamie@email.com":
            Utils.print_error("Email baru tidak boleh sama dengan email saat ini!\n")
            continue
        
        Utils.loading_animation(0.5, "Memeriksa email")
        email_exists = UserRepository.get_user_by_email(email)
        
        if email_exists:
            Utils.print_error("Email tidak tersedia! Gunakan email lain.\n")
            continue
        else:
            Utils.print_success("Email tersedia!")
        
        # konfirmasi
        if Utils.confirm_action(f"Yakin ingin memperbarui email Anda ({email})?"):
            Utils.loading_animation(message="Memperbarui email")
            result = AuthService.update_user_email(user_id, email)

            if result["success"]:
                Utils.print_success(result["message"])
                AppState.set_user_email(email)
                Utils.pause_and_back("Tekan Enter untuk kembali ke menu profil...")
                return
            else:
                Utils.print_error(result["message"])
                continue
        else:
            Utils.clear_screen()
            render_header()
            print("Perubahan dibatalkan. Silakan masukkan email baru lagi \natau 0 untuk batal.\n")
            continue

def ubah_password():
    def render_header():
        Utils.print_header("Ubah Password", show_user=False)
        print("Ketik 0 untuk batal dan kembali ke menu profil.\n")
        print(f"Email Anda saat ini: {AppState.get_user_email() or 'N/A'}\n")
    # tampilkan header sekali di awal
    render_header()
    
    user_id = AppState.get_user_id()
    # user_id = 5
    if not user_id:
        Utils.print_error("ID user tidak valid! Menu ini dilarang diakses.")
        Utils.pause_and_back("Tekan Enter untuk kembali ke menu profil...")
        return
    
    while True:  # loop utama untuk form ubah password
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
            confirm_password = Utils.get_input("Konfirmasi password baru :")
            
            if confirm_password == "0":
                return
            
            if not confirm_password:
                Utils.print_error("Konfirmasi password tidak boleh kosong!\n")
                continue
            
            if password != confirm_password:
                Utils.print_error("Password dan konfirmasi password tidak sesuai!\n")
                continue
            break
        
        # konfirmasi
        if Utils.confirm_action(f"Yakin ingin memperbarui password Anda?"):
            Utils.loading_animation(message="Memperbarui password")
            result = AuthService.update_user_password(user_id, password, confirm_password)

            if result["success"]:
                Utils.print_success(result["message"])
                Utils.pause_and_back("Tekan Enter untuk kembali ke menu profil...")
                return
            else:
                Utils.print_error(result["message"])
        else:
            Utils.clear_screen()
            render_header()
            print("Perubahan dibatalkan. Silakan masukkan password baru lagi \natau 0 untuk batal.\n")