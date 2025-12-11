from business.food_service import FoodService
from state import AppState

def makanan_menu():
    while True:
        print("\n" + "=" * 50)
        print("\n=== MAKANAN ===")
        print("\n" + "=" * 50)
        print("1. Tambah Makanan")
        print("2. Lihat Daftar Makanan")
        print("3. Hapus Makanan")
        print("4. Kembali ke Dashboard")
    
        pilihan = input("Pilih menu [1-4]: ").strip()
    
        if pilihan == "1":
            tambah_makanan()
        elif pilihan == "2":
            lihat_makanan()
        elif pilihan == "3":
            hapus_makanan()
        elif pilihan == "4":
            return
        else:
            print("Pilihan tidak valid!")

def tambah_makanan():
    print("\n" + "-" * 30)
    print("TAMBAH MAKANAN")
    print("-" * 30)
    nama = input("Nama makanan: ").strip()
    jumlah = input("Jumlah: ").strip()
    tanggal_kadaluarsa = input("Tanggal kadaluarsa (YYYY-MM-DD): ").strip()
    kategori = input("Kategori (Protein/Sayuran/Buah/Karbohidrat/Bumbu/Minuman/Lainnya: ").strip()
    
    result = FoodService.tambah_makanan(
        nama, jumlah, tanggal_kadaluarsa, kategori)
    print(result["message"])
    input("Tekan Enter untuk kembali...")

def lihat_makanan():
    print("\n" + "-" * 30)
    print("DAFTAR MAKANAN")
    print("-" * 30)
    
    makanan_list = FoodService.lihat_makanan()
    
    if not makanan_list:
        print("Belum ada makanan yang ditambahkan.")
    else:
        for i, makanan in enumerate(makanan_list, start=1):
            print(f"\n[Makanan ke-{i}] ------------------------------")
            print(f"ID Makanan         : {makanan['id']}")
            print(f"Nama               : {makanan['nama_makanan']}")
            print(f"Jumlah             : {makanan['jumlah']}")
            print(f"Tanggal Kadaluarsa : {makanan['tanggal_kadaluarsa']}")
            print(f"Kategori           : {makanan['kategori']}")
            print("\n----------------------------------")
    input("Tekan Enter untuk kembali...")

def hapus_makanan():
    print("\n" + "-" * 30)
    print("HAPUS MAKANAN")
    print("-" * 30)
    id = input("Masukkan ID makanan yang akan dihapus: ").strip()
    
    result = FoodService.hapus_makanan(id)
    print(result["message"])
    input("Tekan Enter untuk kembali...")