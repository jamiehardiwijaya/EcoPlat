from business.food_service import FoodService
from state import AppState

def makanan_menu():
    while True:
        print("\n" + "=" * 50)
        print("\n=== MAKANAN ===")
        print("\n" + "=" * 50)
        print("1. Tambah Makanan")
        print("2. Lihat Daftar Makanan")
        print("3. Update Makanan")
        print("4. Hapus Makanan")
        print("5. Kembali ke Dashboard")
    
        pilihan = input("Pilih menu [1-5]: ").strip()
    
        if pilihan == "1":
            tambah_makanan()
        elif pilihan == "2":
            lihat_makanan()
        elif pilihan == "3":
            update_makanan()
        elif pilihan == "4":
            hapus_makanan()
        elif pilihan == "5":
            return
        else:
            print("Pilihan tidak valid!")

def tambah_makanan():
    print("\n" + "-" * 30)
    print("TAMBAH MAKANAN")
    print("-" * 30)
    nama = input("Nama makanan: ").strip()
    jumlah = input("Jumlah: ").strip()
    
    while True:
        tanggal_kadaluarsa = input("Tanggal kadaluarsa (YYYY-MM-DD): ").strip()
        
        try:
            from datetime import datetime
            exp_date = datetime.strptime(tanggal_kadaluarsa, '%Y-%m-%d')
            today = datetime.now()
            days_left = (exp_date.date() - today.date()).days
            
            if days_left < 0:
                print(f"⚠️  Peringatan: Makanan sudah kadaluarsa sejak {abs(days_left)} hari yang lalu!")
                konfirmasi = input("Tetap tambahkan? (y/n): ").strip().lower()
                if konfirmasi != 'y':
                    continue
            elif days_left <= 3:
                print(f"⚠️  Peringatan: Makanan akan kadaluarsa dalam {days_left} hari!")
            
            break
            
        except ValueError:
            print("❌ Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
            print("   Contoh: 2024-12-31")
    
    kategori = input("Kategori (Protein/Sayuran/Buah/Karbohidrat/Bumbu/Minuman/Lainnya): ").strip()
    
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

def update_makanan():
    print("\n" + "-" * 30)
    print("UPDATE MAKANAN")
    print("-" * 30)
    
    makanan_list = FoodService.lihat_makanan()
    if not makanan_list:
        print("Belum ada makanan yang bisa diupdate.")
        input("Tekan Enter untuk kembali...")
        return
    
    print("Daftar Makanan:")
    for makanan in makanan_list:
        print(f"ID: {makanan['id']} - {makanan['nama_makanan']} (Jumlah: {makanan['jumlah']})")
    
    id = input("\nMasukkan ID makanan yang akan diupdate: ").strip()
    
    makanan_ada = False
    for makanan in makanan_list:
        if str(makanan['id']) == id:
            makanan_ada = True
            current_nama = makanan['nama_makanan']
            current_jumlah = makanan['jumlah']
            current_tanggal = makanan['tanggal_kadaluarsa']
            current_kategori = makanan['kategori']
            break
    
    if not makanan_ada:
        print("❌ ID makanan tidak ditemukan!")
        input("Tekan Enter untuk kembali...")
        return
    
    print(f"\nUpdate makanan: {current_nama}")
    print("Kosongkan jika tidak ingin mengubah")
    
    nama = input(f"Nama baru [{current_nama}]: ").strip()
    if not nama:
        nama = current_nama
    
    jumlah = input(f"Jumlah baru [{current_jumlah}]: ").strip()
    if not jumlah:
        jumlah = current_jumlah
    
    tanggal_kadaluarsa = input(f"Tanggal kadaluarsa baru [{current_tanggal}]: ").strip()
    if not tanggal_kadaluarsa:
        tanggal_kadaluarsa = current_tanggal
    
    kategori = input(f"Kategori baru [{current_kategori}]: ").strip()
    if not kategori:
        kategori = current_kategori
    
    result = FoodService.update_makanan(id, nama, jumlah, tanggal_kadaluarsa, kategori)
    print(result["message"])
    input("Tekan Enter untuk kembali...")

def hapus_makanan():
    print("\n" + "-" * 30)
    print("HAPUS MAKANAN")
    print("-" * 30)
    
    makanan_list = FoodService.lihat_makanan()
    if not makanan_list:
        print("Belum ada makanan yang bisa dihapus.")
        input("Tekan Enter untuk kembali...")
        return
    
    print("Daftar Makanan:")
    for makanan in makanan_list:
        print(f"ID: {makanan['id']} - {makanan['nama_makanan']}")
    
    id = input("\nMasukkan ID makanan yang akan dihapus: ").strip()
    
    konfirmasi = input(f"Yakin ingin menghapus makanan ID {id}? (y/n): ").strip().lower()
    if konfirmasi != 'y':
        print("Penghapusan dibatalkan.")
        input("Tekan Enter untuk kembali...")
        return
    
    result = FoodService.hapus_makanan(id)
    print(result["message"])
    input("Tekan Enter untuk kembali...")