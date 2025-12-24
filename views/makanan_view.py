from business.food_service import FoodService
from utils.helper import Utils
from datetime import datetime


def makanan_menu():
    menu_items = [
        "➕ Tambah Makanan",
        "📋 Lihat Daftar Makanan",
        "✏️  Update Makanan",
        "🗑️  Hapus Makanan",
        "⬅️  Kembali"
    ]

    while True:
        Utils.clear_screen()
        Utils.print_header("MENU MAKANAN")

        for i, item in enumerate(menu_items, start=1):
            print(f"[{i}] {item}")

        pilihan = input("\nPilih menu [1-5]: ").strip()

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
            Utils.print_error("Pilihan tidak valid!")
            Utils.pause_and_back()

def tambah_makanan():
    while True:
        Utils.clear_screen()
        Utils.print_header("➕ TAMBAH MAKANAN")
        print("Masukkan 0 pada inputan apapun untuk kembali.\n")

        nama = input("Nama makanan : ").strip()
        if nama == "0":
            return
        jumlah = input("Jumlah       : ").strip()
        if jumlah == "0":
            return

        if not nama or not jumlah:
            Utils.print_error("Nama dan/atau jumlah tidak boleh kosong!")
            Utils.pause_and_back()
            continue

        while True:
            tanggal = input("Tanggal kadaluarsa (YYYY-MM-DD): ").strip()
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

        kategori = input("Kategori      : ").strip()
        if kategori == "0":
            return
        if not kategori:
            Utils.print_error("Kategori tidak boleh kosong!")
            Utils.pause_and_back()
            continue

        result = FoodService.tambah_makanan(nama, jumlah, tanggal, kategori)

        if result["success"]:
            Utils.print_success(result["message"])
            Utils.pause_and_clear()
            return
        else:
            Utils.print_error(result["message"])
            Utils.pause_and_back()

def lihat_makanan():
    Utils.clear_screen()
    Utils.print_header("📋 DAFTAR MAKANAN")

    makanan_list = FoodService.lihat_makanan()

    if not makanan_list:
        Utils.print_warning("Belum ada makanan yang ditambahkan.")
        Utils.pause_and_back()
        return

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

    Utils.pause_and_back()

def update_makanan():
    while True:
        Utils.clear_screen()
        Utils.print_header("✏️ UPDATE MAKANAN")

        makanan_list = FoodService.lihat_makanan()
        if not makanan_list:
            Utils.print_warning("Tidak ada makanan untuk diupdate.")
            Utils.pause_and_back()
            return

        for m in makanan_list:
            print(f"{m['id']} - {m['nama_makanan']}")

        print("\nMasukkan ID makanan (0 untuk kembali)")
        id_makanan = input("> ").strip()

        if id_makanan == "0":
            return

        target = next((m for m in makanan_list if str(m["id"]) == id_makanan), None)
        if not target:
            Utils.print_error("ID makanan tidak ditemukan!")
            Utils.pause_and_back()
            continue

        print("\n(Kosongkan jika tidak ingin mengubah)")
        nama = input(f"Nama [{target['nama_makanan']}]: ").strip() or target["nama_makanan"]
        jumlah = input(f"Jumlah [{target['jumlah']}]: ").strip() or target["jumlah"]
        tanggal = input(f"Tanggal [{target['tanggal_kadaluarsa']}]: ").strip() or target["tanggal_kadaluarsa"]
        kategori = input(f"Kategori [{target['kategori']}]: ").strip() or target["kategori"]

        if not Utils.confirm_action("Simpan perubahan?"):
            Utils.print_warning("Update dibatalkan.")
            Utils.pause_and_back()
            return

        result = FoodService.update_makanan(
            id_makanan, nama, jumlah, tanggal, kategori
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

        for m in makanan_list:
            print(f"{m['id']} - {m['nama_makanan']}")

        print("\nMasukkan ID makanan (0 untuk kembali)")
        id_makanan = input("> ").strip()

        if id_makanan == "0":
            return

        target = next((m for m in makanan_list if str(m["id"]) == id_makanan), None)
        if not target:
            Utils.print_error("ID makanan tidak ditemukan!")
            Utils.pause_and_back()
            continue

        print(f"\nNama     : {target['nama_makanan']}")
        print(f"Jumlah   : {target['jumlah']}")
        print(f"Kategori : {target['kategori']}")
        print(f"Exp Date : {target['tanggal_kadaluarsa']}")

        if not Utils.confirm_action("Yakin ingin menghapus makanan ini?"):
            Utils.print_warning("Penghapusan dibatalkan.")
            Utils.pause_and_back()
            return

        result = FoodService.hapus_makanan(id_makanan)

        if result["success"]:
            Utils.print_success(result["message"])
            Utils.pause_and_clear()
            return
        else:
            Utils.print_error(result["message"])
            Utils.pause_and_back()