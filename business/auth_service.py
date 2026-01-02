import bcrypt
from databases.user_repository import UserRepository
from state import AppState

class AuthService:
    @staticmethod
    def register_user(nama, email, password, confirm_password):
        if not nama or not email or not password:
            return {"success": False, "message": "Semua field harus diisi!"}
        
        if password != confirm_password:
            return {"success": False, "message": "Password dan konfirmasi password tidak sesuai!"}
        
        if len(password) < 6:
            return {"success": False, "message": "Password minimal 6 karakter!"}
        
        existing_user = UserRepository.get_user_by_email(email)
        if existing_user:
            return {"success": False, "message": "Email sudah terdaftar!"}
        
        try:
            id_user = UserRepository.add_user(nama, email, password)
            return {"success": True, "message": "Registrasi berhasil! Silakan login terlebih dahulu.", "user_id": id_user}
        except Exception as e:
            return {"success": False, "message": f"Terjadi kesalahan: {e}"}
        
    @staticmethod
    def login_user(email, password):
        if not email or not password:
            return {"success": False, "message": "Email dan password harus diisi!"}
        
        user = UserRepository.verify_user(email, password)
        
        if user:
            AppState.login(user)
            return {
                "success": True, 
                "message": f"Login berhasil! Selamat datang, {user['nama']}", 
                "user": user
            }
        else:
            return {"success": False, "message": "Email atau password salah!"}
            
    @staticmethod
    def logout_user():
        AppState.logout()
        return {"success": True, "message": "Logout berhasil!"}
        
    @staticmethod
    def lupa_password(email, password, confirm_password):
        if not password or not confirm_password:
            return {"success": False, "message": "Password tidak boleh kosong"}

        if password != confirm_password:
            return {"success": False, "message": "Password dan konfirmasi tidak sama"}

        if len(password) < 6:
            return {"success": False, "message": "Password minimal 6 karakter"}

        user = UserRepository.get_user_by_email(email)
        if not user:
            return {"success": False, "message": "Email tidak terdaftar"}

        UserRepository.update_password_by_email(email, password)
        return {"success": True, "message": "Password berhasil diperbarui. \n\nSilakan login dengan password baru Anda."}    
    
    @staticmethod
    def update_user_name(user_id, new_name):
        if not user_id:
            return {"success": False, "message": "ID user tidak valid"}
        
        if not new_name:
            return {"success": False, "message": "Nama tidak boleh kosong"}
        
        try:
            UserRepository.update_user_name(user_id, new_name)
            return {"success": True, "message": "Nama berhasil diperbarui"}
        except Exception as e:
            return {"success": False, "message": "Gagal memperbarui nama. Silakan coba lagi."}
            
    @staticmethod
    def update_user_email(user_id, new_email):
        if not user_id:
            return {"success": False, "message": "ID user tidak valid"}
        
        if not new_email:
            return {"success": False, "message": "Email tidak boleh kosong"}
        
        existing_user = UserRepository.get_user_by_email(new_email)
        if existing_user:
            return {"success": False, "message": "Email sudah terdaftar oleh user lain"}
        
        try:
            UserRepository.update_user_email(user_id, new_email)
            return {"success": True, "message": "Email berhasil diperbarui"}
        except Exception as e:
            return {"success": False, "message": "Gagal memperbarui email. Silakan coba lagi."}
        
    @staticmethod
    def update_user_password(user_id, new_password, confirm_password):
        if not user_id:
            return {"success": False, "message": "ID user tidak valid"}
        
        if not new_password:
            return {"success": False, "message": "Password tidak boleh kosong"}
        
        if len(new_password) < 6:
            return {"success": False, "message": "Password minimal 6 karakter"}
            
        if new_password != confirm_password:
            return {"success": False, "message": "Password dan konfirmasi password tidak sesuai"}
        
        try:
            UserRepository.update_password_by_id(user_id, new_password)
            return {"success": True, "message": "Password berhasil diperbarui"}
        except Exception as e:
            return {"success": False, "message": "Gagal memperbarui password. Silakan coba lagi."}