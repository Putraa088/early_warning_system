from models.UserModel import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self, email, password):
        """Authenticate user login"""
        try:
            if not email or not password:
                return False, "Email dan password harus diisi"
            
            if not self._is_valid_email(email):
                return False, "Format email tidak valid"
            
            user = self.user_model.authenticate_user(email, password)
            
            if user:
                return True, user
            else:
                return False, "Email atau password salah"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def register(self, email, password, full_name, confirm_password):
        try:
            if not all([email, password, full_name, confirm_password]):
                return False, "Semua field harus diisi"
            
            if not self._is_valid_email(email):
                return False, "Format email tidak valid"
            
            if password != confirm_password:
                return False, "Password dan konfirmasi password tidak sama"
            
            if len(password) < 6:
                return False, "Password minimal 6 karakter"
            
            if len(full_name) < 3:
                return False, "Nama lengkap minimal 3 karakter"
            
            user_id = self.user_model.create_user(email, password, full_name)
            if user_id:
                return True, "Registrasi berhasil! Silakan login."
            else:
                return False, "Gagal membuat akun"
                
        except Exception as e:
            return False, str(e)

    def _is_valid_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def logout(self):

        return True, "Logout berhasil"
