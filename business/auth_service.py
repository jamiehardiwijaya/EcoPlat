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
    