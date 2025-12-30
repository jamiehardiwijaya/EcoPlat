from business.food_service import FoodService
from business.recovery_service import RecoveryService
from state import AppState
from utils.helper import Utils
from datetime import datetime

list_kategori = [
            "Sayur",
            "Daging",
            "Minuman",
            "Buah",
            "Lainnya"
        ]
def makanan_menu():
    menu_items = [
        "📋 Lihat Daftar Makanan",
        "➕ Tambah Makanan",
        "✏️  Update Makanan",
        "🗑️  Hapus Makanan",
        "🔄 Pulihkan Makanan", 
        "⬅️  Kembali"
    ]

    while True:
        Utils.clear_screen()
        Utils.print_header("MENU MAKANAN")

        pilihan = Utils.pilih_menu(menu_items)

        if pilihan == 1:
            lihat_makanan()
        elif pilihan == 2:
            tambah_makanan()
        elif pilihan == 3:
            update_makanan()
        elif pilihan == 4:
            hapus_makanan()
        elif pilihan == 5:  
            pulihkan_makanan()
        elif pilihan == 6:
            return
        else:
            Utils.print_error("Pilihan tidak valid!")


def tambah_makanan():
    while True:
        Utils.clear_screen()
        Utils.print_header("➕ TAMBAH MAKANAN")
        print("Masukkan 0 pada inputan apapun untuk kembali.\n")

        while True:
            nama = input("Nama makanan : ").strip()
            if nama == "0":
                return
            if not nama:
                Utils.print_error("Nama makanan tidak boleh kosong!")
                continue
            break
        
        while True:
            jumlah = input("Jumlah       : ").strip()
            if jumlah == "0":
                return

            if not jumlah:
                Utils.print_error("Jumlah tidak boleh kosong!")
                continue
            break   

        while True:
            tanggal = input("Tanggal kadaluarsa (YYYY-MM-DD), Contoh --> 2026-01-01 : ").strip()
            if tanggal == "0":
                return
            if not tanggal:
                Utils.print_error("Tanggal kadaluarsa tidak boleh kosong!")
                continue
            try:
                exp_date = datetime.strptime(tanggal, "%Y-%m-%d")
                days_left = (exp_date.date() - datetime.now().date()).days

                if days_left < 0:
                    print(f"⚠️  Makanan sudah kadaluarsa {abs(days_left)} hari.")
                    if input("Tetap tambahkan? (y/n): ").lower() != "y":
                        continue
                elif days_left <= 3:
                    print(f"⚠️  Makanan akan kadaluarsa dalam {days_left} hari.")
                break
            except ValueError:
                print("❌ Format tanggal salah! Gunakan YYYY-MM-DD")
                print("Contoh format tanggal : 2026-01-01")
        while True:
            print("Kategori")
            for i, kat in enumerate(list_kategori, start=1):
                print(f"{i}. {kat}")
            print("0. Kembali")

            kategori = input("\nPilih kategori: ").strip()

            if kategori == "0":
                return
            if not kategori:
                Utils.print_error("Kategori tidak boleh kosong!")
                continue
            if not kategori.isdigit() or not (1 <= int(kategori) <= len(list_kategori)):
                Utils.print_error("Pilihan kategori tidak valid!")
                continue
            break

        kategori = list_kategori[int(kategori) - 1]

        result = FoodService.tambah_makanan(nama, jumlah, tanggal, kategori)

        if result["success"]:
            Utils.print_success(result["message"])
            Utils.pause_and_clear()
            return
        else:
            Utils.print_error(result["message"])
            Utils.pause_and_back()

def lihat_semua_makanan(makanan_list):
    for i, m in enumerate(makanan_list, start=1):
        print(f"""
[{i}] -------------------------------
ID         : {m['id']}
Nama       : {m['nama_makanan']}
Jumlah     : {m['jumlah']}
Kadaluarsa : {m['tanggal_kadaluarsa']}
Kategori   : {m['kategori']}
-----------------------------------
""")
        
def lihat_makanan():
    Utils.clear_screen()
    Utils.print_header("📋 DAFTAR MAKANAN")

    from business.recovery_service import RecoveryService
    from state import AppState
    
    user_id = AppState.get_user_id()
    if user_id:
        deleted_foods = RecoveryService.get_deleted_foods(user_id)
        if deleted_foods:
            print(f"💡 Info: Ada {len(deleted_foods)} makanan yang dapat dipulihkan.")
            print(f"         Gunakan menu '🔄 Pulihkan Makanan' untuk mengembalikannya.\n")

    makanan_list = FoodService.lihat_makanan()

    if not makanan_list:
        Utils.print_warning("Belum ada makanan yang ditambahkan.")
        Utils.pause_and_back()
        return

    while True:
        print("Pilih opsi tampilan:")
        print("1. Tampilkan semua makanan")
        print("2. Cari Makanan")
        print("0. Kembali ke menu sebelumnya")

        choice = input("\nPilihan Anda: ").strip()

        if choice == "1":
            Utils.print_header("📋 DAFTAR SEMUA MAKANAN")
            lihat_semua_makanan(makanan_list)
            Utils.pause_and_back()
            return
        
        elif choice == "2":
            keyword = input("Cari (nama/kategori): ").strip().lower()
            if keyword == "0":
                return
            
            hasil = [m for m in makanan_list if keyword in m['nama_makanan'].lower() or keyword in m['kategori'].lower()]
                    
            if not hasil:
                Utils.print_warning("Tidak ada makanan yang sesuai dengan kata kunci.")
            else:
                Utils.clear_screen()
                Utils.loading_animation()
                Utils.print_header(f"🔍 HASIL PENCARIAN UNTUK '{keyword}'")
                lihat_semua_makanan(hasil)
            
            Utils.pause_and_back()
            return
        
        elif choice == "0":
            return
        else:
            Utils.print_error("Pilihan tidak valid!")

def update_makanan():
    while True:
        Utils.clear_screen()
        Utils.print_header("✏️ UPDATE MAKANAN")
        print("Ketik 0 pada inputan apapun untuk kembali ke menu sebelumnya\n")

        makanan_list = FoodService.lihat_makanan()
        if not makanan_list:
            Utils.print_warning("Tidak ada makanan untuk diupdate.")
            Utils.pause_and_back()
            return

        for i, m in enumerate(makanan_list, start=1):
            print(f"{i}. {m['nama_makanan']}")

        pilihan = input("\nPilih nomor makanan: ").strip()

        if pilihan == "0":
            return

        if not pilihan.isdigit() or not (1 <= int(pilihan) <= len(makanan_list)):
            Utils.print_error("Pilihan tidak valid!")
            Utils.pause_and_back()
            continue

        target = makanan_list[int(pilihan) - 1]

        print("\n(Kosongkan jika tidak ingin mengubah)")
        nama = input(f"Nama [{target['nama_makanan']}]: ").strip() or target["nama_makanan"]
        if nama == "0":
            return
        jumlah = input(f"Jumlah [{target['jumlah']}]: ").strip() or target["jumlah"]
        if jumlah == "0":
            return
        while True:
            tanggal = input(f"Tanggal [{target['tanggal_kadaluarsa']}]: ").strip() or target["tanggal_kadaluarsa"]
            if tanggal == "0":
                return
            try:
                exp_date = datetime.strptime(tanggal, "%Y-%m-%d")
                days_left = (exp_date.date() - datetime.now().date()).days

                if days_left < 0:
                    print(f"⚠️  Makanan sudah kadaluarsa {abs(days_left)} hari.")
                    if input("Tetap tambahkan? (y/n): ").lower() != "y":
                        continue
                elif days_left <= 3:
                    print(f"⚠️  Makanan akan kadaluarsa dalam {days_left} hari.")
                break
            except ValueError:
                print("❌ Format tanggal salah! Gunakan YYYY-MM-DD")
                print("Contoh format tanggal : 2026-01-01")
        
        while True:
            print("Kategori")
            for i, kat in enumerate(list_kategori, start=1):
                print(f"{i}. {kat}")

            kategori = input(f"Kategori [{target['kategori']}]: ").strip() 

            if kategori == "0":
                return
            
            if kategori == "":
                kategori = target["kategori"]
            elif kategori.isdigit() and 1 <= int(kategori) <= len(list_kategori):
                kategori = list_kategori[int(kategori) - 1]
            else:
                Utils.print_error("Pilihan kategori tidak valid!")
                Utils.pause_and_back()
                continue

            if not Utils.confirm_action("Simpan perubahan?"):
                Utils.print_warning("Update dibatalkan.")
                Utils.pause_and_back()
                return

            result = FoodService.update_makanan(
                target["id"],nama, jumlah, tanggal, kategori
            )

            if result["success"]:
                Utils.print_success(result["message"])
                Utils.pause_and_clear()
                return
            else:
                Utils.print_error(result["message"])
                Utils.pause_and_back()

def hapus_makanan():
    while True:
        Utils.clear_screen()
        Utils.print_header("🗑️ HAPUS MAKANAN")

        makanan_list = FoodService.lihat_makanan()
        if not makanan_list:
            Utils.print_warning("Tidak ada makanan untuk dihapus.")
            Utils.pause_and_back()
            return

        for i, m in enumerate(makanan_list, start=1):
            print(f"{i}. {m['nama_makanan']}")

        print("\nMasukkan nomor makanan (0 untuk kembali)")
        pilihan = input("> ").strip()

        if pilihan == "0":
            return

        if not pilihan.isdigit() or not (1 <= int(pilihan) <= len(makanan_list)):
            Utils.print_error("Pilihan tidak valid!")
            Utils.pause_and_back()
            continue

        target = makanan_list[int(pilihan) - 1]

        print(f"\nNama     : {target['nama_makanan']}")
        print(f"Jumlah   : {target['jumlah']}")
        print(f"Kategori : {target['kategori']}")
        print(f"Exp Date : {target['tanggal_kadaluarsa']}")
        
        print(f"\n💡 Informasi:")
        print(f"• Makanan akan dicatat di histori")
        print(f"• Dapat dipulihkan nanti melalui menu '🔄 Pulihkan Makanan'")
        print(f"• Data akan disimpan selama 30 hari")

        if not Utils.confirm_action("Yakin ingin menghapus makanan ini?"):
            Utils.print_warning("Penghapusan dibatalkan.")
            Utils.pause_and_back()
            return

        result = FoodService.hapus_makanan(target["id"])

        if result["success"]:
            Utils.print_success(result["message"])
            print(f"\n📝 Catatan: Makanan dapat dipulihkan melalui menu 'Pulihkan Makanan'")
            Utils.pause_and_clear()
            return
        else:
            Utils.print_error(result["message"])
            Utils.pause_and_back()

def pulihkan_makanan():
    """Menu untuk memulihkan makanan yang telah dihapus"""
    
    while True:
        Utils.clear_screen()
        Utils.print_header("🔄 PULIHKAN MAKANAN YANG DIHAPUS")
        
        user_id = AppState.get_user_id()
        if not user_id:
            Utils.print_error("Anda harus login terlebih dahulu!")
            Utils.pause_and_back()
            return
        
        deleted_foods = RecoveryService.get_deleted_foods(user_id)
        
        if not deleted_foods:
            Utils.print_warning("Tidak ada makanan yang dapat dipulihkan.")
            print("\n0. Kembali ke Menu Makanan")
            choice = input("\nPilih: ").strip()
            if choice == "0":
                return
            continue
        
        print(f"\nDitemukan {len(deleted_foods)} makanan yang dapat dipulihkan:\n")
        print("═" * 60)

        for i, food in enumerate(deleted_foods, 1):
            nama = food['nama_makanan'][:20] 
            print(f"{i}. {nama:<20} | Jml: {food['jumlah']:>3} | Kategori: {food['kategori']:<10}")
        
        print("═" * 60)
        print("\n📋 Pilih nomor makanan untuk dipulihkan")
        print("0. Kembali ke Menu Makanan")
        
        choice = input("\nPilih : ").strip()
        
        if choice == "0":
            return
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(deleted_foods):
                food_to_recover = deleted_foods[choice_num - 1]

                confirm = input(f"\nPulihkan '{food_to_recover['nama_makanan']}'? (y/n): ").lower()
                if confirm == 'y':
                    result = RecoveryService.recover_food(food_to_recover['id'])
                    if result["success"]:
                        Utils.print_success(result["message"])
                    else:
                        Utils.print_error(result["message"])
                    Utils.pause_and_back()
                    return
                else:
                    Utils.print_warning("Pemulihan dibatalkan.")
                    Utils.pause_and_back()
            else:
                Utils.print_error("Nomor tidak valid!")
                Utils.pause_and_back()
                
        except ValueError:
            Utils.print_error("Masukkan angka yang valid!")
            Utils.pause_and_back()