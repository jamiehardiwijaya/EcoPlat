from state import AppState
from utils.helper import Utils

def show_profil():
    Utils.print_header("Profil Saya", show_user=False)
    
    print("Profil Anda\n")
    print(f"Nama  : {AppState.get_user_name() or 'N/A'}")
    print(f"Email : {AppState.get_user_email() or 'N/A'}")
    
    Utils.pause_and_back("Tekan Enter untuk kembali ke dashboard utama...")