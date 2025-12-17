# from business.auth_service import AuthService
# from databases.user_repository import UserRepository
# from views.dashboard_view import show_dashboard, show_main_app
# from utils.helper import Utils

# def show_auth_screen():
#     Utils.print_header("Food Waste Manager")

# def show_auth_menu():
#     menu = [
#         "🔑 Login",
#         "📝 Register",
#         "❌ Keluar Aplikasi"
#     ]

#     print("Buat akun atau login untuk mulai mengelola makanan Anda dan mengurangi food waste!\n")
    
#     choice = Utils.pilih_menu(menu)
    
#     if choice == 1:
#         handle_login()
#     elif choice == 2:
#         handle_register()
#     elif choice == 3:
#         confirm_exit()
#     else:
#         Utils.print_error("Pilihan tidak valid!")

# def handle_login():
#     Utils.print_header("Login")
   
#     email    = Utils.get_input   ("Email    :")
#     password = Utils.get_password("Password :")
    
#     result = AuthService.login_user(email, password)
    
#     if result["success"]:
#         Utils.print_success(result["message"])
#         Utils.pause_and_clear()
#         show_main_app()
#     else:
#         Utils.print_error(result["message"])
#         Utils.pause_and_back()

# def handle_register(): 
#     Utils.print_header("Register")
    
#     # Utils.print_info("Buat akun baru untuk mulai mengelola makanan")
#     # print()  # Spacing
    
#     nama = Utils.get_input("Nama lengkap\t:")
#     if not nama:
#         Utils.print_error("Nama tidak boleh kosong!\n")
#         return
    
#     while True:
#         email = Utils.get_input("Email \t\t:")
    
#         if not email:
#             Utils.print_error("Nama tidak boleh kosong!\n")
#             continue 
        
#         if "@" not in email or "." not in email:
#             Utils.print_error("Format email tidak valid!")
#             print("Contoh format email: abc@gmail.com; xyz@upi.edu\n")
#             continue
        
#         Utils.loading_animation(0.5, "Memeriksa email")
#         email_exists = UserRepository.get_user_by_email(email)
        
#         if email_exists:
#             Utils.print_error("Email sudah terdaftar!\n")
#             continue
#         else:
#             Utils.print_success("Email tersedia!\n")
#             break
            
#     while True:
#         password = Utils.get_input("Password (min 6 karakter) :")
        
#         if len(password) < 6:
#             Utils.print_error("Password minimal 6 karakter!\n")
#             continue
#         break
    
#     while True:
#         confirm_password = Utils.get_input("Konfirmasi password       :")
        
#         if password != confirm_password:
#             Utils.print_error("Password dan konfirmasi password tidak sesuai!\n")
#             continue
#         break
    
#     Utils.loading_animation(message="Memproses registrasi")
     
#     result = AuthService.register_user(nama, email, password, confirm_password)
    
#     if result["success"]:
#         # Utils.wait(1, "Login otomatis")
        
#         # # Auto login
#         # login_result = AuthService.login_user(email, password)
#         # if login_result["success"]:
#         Utils.print_success(result["message"])
#         Utils.pause_and_clear()
#         show_main_app()
#     else:
#         Utils.print_error(result["message"])
#         Utils.pause_and_back()

        
# while True:
#     show_auth_screen()
#     show_auth_menu()