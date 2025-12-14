import os
import sys
import time
import maskpass  # Untuk input password yang tersembunyi
from typing import Optional

class Utils:
    """Utility class untuk formatting CLI"""
    
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title):
        Utils.clear_screen()
        print("=" * 60)
        print(f"    🌱 ECOPLAT - {title}")
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