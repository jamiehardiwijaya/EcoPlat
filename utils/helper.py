import os
import sys
import time
import maskpass  # Untuk input password yang tersembunyi
from typing import Optional
from state import AppState

class Utils:
    """Utility class untuk formatting CLI"""
    
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title, show_user=True, clear=True):
        if clear:
            Utils.clear_screen()
        user_name = AppState.get_user_name()
        print("=" * 60)
        print(f"    🌱 ECOPLAT - {title}")
        if AppState.is_logged_in() and show_user:
            print(f"    User: {user_name}")
        print("=" * 60)
    
    @staticmethod
    def print_menu(title, options):
        """Print menu dengan format"""
        print(f"\n{title}")
        print("-" * 40)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
    
    @staticmethod
    def print_success(message):
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message):
        print(f"❌ {message}")
    
    @staticmethod
    def print_warning(message):
        print(f"⚠️  {message}")
    
    @staticmethod
    def get_input(prompt):
        return input(f"{prompt} ").strip()
    
    @staticmethod
    def get_password(prompt):
        """Get password input (hidden)"""
        return maskpass.askpass(prompt=f"{prompt} ", mask='*')
    
    @staticmethod
    def confirm_action(message):
        """Konfirmasi aksi dengan y/n"""
        response = input(f"{message} (y/n): ").strip().lower()
        return response == 'y'
    
    @staticmethod
    def print_table(headers, data):
        """Print tabel sederhana"""
        # Hitung lebar kolom
        col_widths = [len(str(h)) for h in headers]
        
        for row in data:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print header
        header_line = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
        print("\n" + "-" * len(header_line))
        print(header_line)
        print("-" * len(header_line))
        
        # Print data
        for row in data:
            row_line = " | ".join(f"{str(cell):<{w}}" for cell, w in zip(row, col_widths))
            print(row_line)
        
        print("-" * len(header_line) + "\n")
        
    @staticmethod
    def pause(message: str = "Tekan Enter untuk melanjutkan...", clear_after: bool = False):
        """
        Pause execution dengan pesan custom
        
        Args:
            message: Pesan yang ditampilkan
            clear_after: Jika True, clear screen setelah user tekan Enter
        """
        input(f"\n{message}")
        if clear_after:
            Utils.clear_screen()
    
    @staticmethod
    def pause_and_clear(message: str = "Tekan Enter untuk melanjutkan..."):
        """Pause lalu clear screen"""
        Utils.pause(message, clear_after=True)
    
    @staticmethod
    def pause_and_back(message: str = "Tekan Enter untuk kembali..."):
        """Pause dengan pesan 'kembali'"""
        Utils.pause(message)
    
    @staticmethod
    def wait(seconds: float = 2, message: Optional[str] = None):
        """
        Wait dengan loading animation
        
        Args:
            seconds: Durasi dalam detik
            message: Pesan yang ditampilkan (optional)
        """
        if message:
            print(f"\n{message}", end="", flush=True)
        
        for _ in range(int(seconds * 10)):
            print(".", end="", flush=True)
            time.sleep(0.1)
        print()
    
    @staticmethod
    def confirm_exit():
        """Konfirmasi keluar aplikasi"""
        if Utils.confirm_action("Yakin ingin keluar aplikasi?"):
            print("\n👋 Terima kasih telah menggunakan EcoPlat!")
            sys.exit(0)
    
    @staticmethod
    def press_any_key():
        """Tekan sembarang tombol untuk continue (cross-platform)"""
        if os.name == 'nt':  # Windows
            os.system('pause')
        else:  # Linux/Mac
            os.system('read -n1 -r -p "Tekan sembarang tombol untuk melanjutkan..." key')
    
    @staticmethod
    def loading_animation(duration=1.5, message="Memuat"):
        """Animasi loading sederhana"""
        print(f"\n{message}", end="", flush=True)
        animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        
        start_time = time.time()
        i = 0
        while time.time() - start_time < duration:
            print(f"\r{message} {animation[i % len(animation)]}", end="", flush=True)
            time.sleep(0.1)
            i += 1
        print(f"\r{message} ‼️", " " * 20)  # Clear line
        
    def pilih_menu(menu_items):
        """
        Menampilkan daftar menu secara dinamis dan meminta input pilihan yang valid
        dari pengguna.

        Args:
            menu_items (list): List berisi string item menu.

        Returns:
            int: Angka pilihan menu yang valid (1, 2, 3, dst.).
        """
    
        # 1. Tampilkan Header
        print("\n=== MENU UTAMA ===")

        # 2. Mencetak Menu Secara Dinamis
        for index, item in enumerate(menu_items, 1):
            print(f"{index}. {item}")

        # 3. Hitung Jumlah Menu dan Buat Rentang Pilihan
        total_items = len(menu_items) 
        pilihan_range = f"1-{total_items}" 

        # 4. Ambil Input dengan Loop Pengecekan Validitas
        while True:
            choice = input(f"\nPilih menu [{pilihan_range}]: ").strip()
            
            # Pengecekan Input
            if choice.isdigit():
                choice_num = int(choice)
                
                # Pastikan input berada dalam rentang yang benar
                if 1 <= choice_num <= total_items:
                    return choice_num # Mengembalikan angka pilihan yang valid
                else:
                    print(f"❌ Pilihan tidak valid. Silakan masukkan angka antara 1 sampai {total_items}.")
            else:
                print("❌ Masukkan hanya angka.")
                
    @staticmethod
    def confirm_action(message):
        """Meminta konfirmasi dari user"""
        while True:
            response = input(f"\n{message} (y/n): ").strip().lower()
            if response in ['y', 'ya', 'yes']:
                return True
            elif response in ['n', 'tidak', 'no']:
                return False
            else:
                print("Masukkan 'y' untuk ya atau 'n' untuk tidak")
    
    @staticmethod
    def print_recovery_info(message):
        """Mencetak informasi tentang pemulihan"""
        print(f"\n🔄 INFO PEMULIHAN: {message}")
                
    def greeting_user():
        """Menampilkan pesan sapaan kepada pengguna yang telah login."""
        user_name = AppState.get_user_name() or "Guest"
        print(f"\nSelamat datang di EcoPlat, {user_name}! 🤩")

    @staticmethod
    def parse_jumlah(jumlah):
        """
        Mengubah jumlah (int / str bebas) menjadi integer aman untuk perhitungan.
        """
        if isinstance(jumlah, int):
            return jumlah

        if isinstance(jumlah, str):
            angka = [int(x) for x in jumlah.split() if x.isdigit()]
            return sum(angka)
        return 0
    
    @staticmethod
    def _normalize_types(df):
        df['id'] = df['id'].astype('Int64')
        df['user_id'] = df['user_id'].astype('Int64')
        df['jumlah'] = df['jumlah'].astype('Int64')
        df['is_recovered'] = df['is_recovered'].astype('Int64')

        df['recovered_at'] = df['recovered_at'].astype(str)
        df['deleted_at'] = df['deleted_at'].astype(str)
        df['tanggal_kadaluarsa'] = df['tanggal_kadaluarsa'].astype(str)
        return df

