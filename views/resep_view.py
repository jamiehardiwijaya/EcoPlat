import datetime
from business.food_service import FoodService
from business.recipe_service import RecipeService
from business.recovery_service import RecoveryService
from state import AppState
from utils.helper import Utils
from views.makanan_view import lihat_semua_makanan

def resep_menu():
    menu_items = [
        "➕ Tambah Resep",
        "📋 Lihat Resep Saya",
        "🌍 Lihat Semua Resep",
        "✏️  Update Resep",
        "🗑️  Hapus Resep",
        "🔄 Pulihkan Resep",
        "⬅️  Kembali"
    ]

    while True:
        Utils.clear_screen()
        Utils.print_header("MENU RESEP")

        pilihan = Utils.pilih_menu(menu_items)

        if pilihan == 1:
            tambah_resep()
        elif pilihan == 2:
            lihat_resep_saya()
        elif pilihan == 3:
            lihat_semua_resep()
        elif pilihan == 4:
            update_resep()
        elif pilihan == 5:
            hapus_resep()
        elif pilihan == 6:
            pulihkan_resep()
        elif pilihan == 7:
            return
        else:
            Utils.print_error("Pilihan tidak valid!")

def tambah_resep():
    Utils.clear_screen()
    Utils.print_header("➕ TAMBAH RESEP")
    print("Ketik 0 pada inputan apapun untuk kembali ke menu sebelumnya\n")

    while True:
        nama = input("Nama resep      : ").strip()
        if nama == "0":
            return
        deskripsi = input("Deskripsi resep : ").strip()
        if deskripsi == "0":    
            return

        if not nama or not deskripsi:
            Utils.print_error("Nama dan/atau deskripsi tidak boleh kosong!")
            Utils.pause_and_back()
            Utils.clear_screen()
            Utils.print_header("➕ TAMBAH RESEP")
            continue
        break

    while True:
        print("\nMasukkan bahan (pisahkan dengan koma)")
        bahan_input = input("Contoh: telur,bawang,cabai\n> ").strip()
        if bahan_input == "0":
            return

        daftar_bahan = [b.strip() for b in bahan_input.split(",") if b.strip()]

        if not daftar_bahan:
            Utils.print_error("Minimal satu bahan harus diisi!")
            Utils.pause_and_back()
            continue
        break

    result = RecipeService.tambah_resep(nama, deskripsi, daftar_bahan)

    if result["success"]:
        Utils.print_success(result["message"])
        Utils.pause_and_clear()
    else:
        Utils.print_error(result["message"])
        Utils.pause_and_back()

def lihat_resep(resep_list):
    for i, r in enumerate(resep_list, start=1):
        bahan = ", ".join(r["bahan"]) if r["bahan"] else "Tidak ada bahan"
        print(f"""
[{i}] -------------------------------
ID   : {r['id']}
Nama : {r['nama_resep']}
Desk : {r['deskripsi']}
Bahan: {bahan}
-----------------------------------
""")
        
def lihat_resep_saya():
    Utils.clear_screen()
    Utils.print_header("📋 RESEP SAYA")

    resep_list = RecipeService.lihat_resep_saya()

    if not resep_list:
        Utils.print_warning("Belum ada resep.")
        Utils.pause_and_back()
        return
    
    while True:
        print("Pilih opsi tampilan:")
        print("1. Tampilkan semua resep")
        print("2. Cari Resep")
        print("0. Kembali ke menu sebelumnya")

        choice = input("\nPilihan Anda: ").strip()

        if choice == "1":
            Utils.print_header("📋 DAFTAR SEMUA RESEP")
            lihat_resep(resep_list)
            Utils.pause_and_back()
            return
        
        elif choice == "2":
            keyword = input("Cari (nama): ").strip().lower()
            if keyword == "0":
                return

            hasil = [m for m in resep_list if keyword in m['nama_resep'].lower()]
                    
            if not hasil:
                Utils.print_warning("Tidak ada resep yang sesuai dengan kata kunci.")
            else:
                Utils.clear_screen()
                Utils.loading_animation()
                Utils.print_header(f"🔍 HASIL PENCARIAN UNTUK '{keyword}'")
                lihat_resep(hasil)
            
            Utils.pause_and_back()
            return
        
        elif choice == "0":
            return
        else:
            Utils.print_error("Pilihan tidak valid!")

def lihat_semua_resep():
    Utils.clear_screen()
    Utils.print_header("🌍 SEMUA RESEP")

    resep_list = RecipeService.lihat_semua_resep()

    if not resep_list:
        Utils.print_warning("Belum ada resep.")
        Utils.pause_and_back()
        return

    for i, r in enumerate(resep_list, start=1):
        bahan = ", ".join(r["bahan"]) if r["bahan"] else "Tidak ada bahan"
        print(f"""
[{i}] -------------------------------
Nama     : {r['nama_resep']}
Pembuat  : {r['pembuat']}
Deskripsi: {r['deskripsi']}
Bahan    : {bahan}
-----------------------------------
""")

    Utils.pause_and_back()

def update_resep():
    while True:
        Utils.clear_screen()
        Utils.print_header("✏️ UPDATE RESEP")
        print("Ketik 0 pada inputan apapun untuk kembali ke menu sebelumnya\n")

        resep_menu = RecipeService.lihat_resep_saya()
        if not resep_menu:
            Utils.print_warning("Tidak ada resep untuk diupdate.")
            Utils.pause_and_back()
            return

        for m in resep_menu:
            print(f"{m['id']} - {m['nama_resep']}")

        print("\nMasukkan ID resep (0 untuk kembali)")
        id_resep = input("> ").strip()

        if id_resep == "0":
            return

        target = next((m for m in resep_menu if str(m["id"]) == id_resep), None)
        if not target:
            Utils.print_error("ID resep tidak ditemukan!")
            Utils.pause_and_back()
            continue

        print("\n(Kosongkan jika tidak ingin mengubah)")
        nama = input(f"Nama [{target['nama_resep']}]: ").strip() or target["nama_resep"]
        if nama == "0":
            return
        deskripsi = input(f"Deskripsi [{target['deskripsi']}]: ").strip() or target["deskripsi"]
        if deskripsi == "0":
            return
        bahan_input = input(f"Bahan (pisahkan koma) [{', '.join(target['bahan'])}]: ").strip()
        if bahan_input == "0":
            return

        if bahan_input:
            daftar_bahan = [b.strip() for b in bahan_input.split(",") if b.strip()]
        else:
            daftar_bahan = target["bahan"]

        if not Utils.confirm_action("Simpan perubahan?"):
            Utils.print_warning("Update dibatalkan.")
            Utils.pause_and_back()
            return

        result = RecipeService.update_resep(
            id_resep, nama, deskripsi, daftar_bahan
        )

        if result["success"]:
            Utils.print_success(result["message"])
            Utils.pause_and_clear()
            return
        else:
            Utils.print_error(result["message"])
            Utils.pause_and_back()

def hapus_resep():
    from business.recovery_resep_service import RecipeRecoveryService

    while True:
        Utils.clear_screen()
        Utils.print_header("🗑️ HAPUS RESEP")

        resep_list = RecipeService.lihat_resep_saya()

        if not resep_list:
            Utils.print_warning("Tidak ada resep untuk dihapus.")
            Utils.pause_and_back()
            return

        for r in resep_list:
            print(f"{r['id']} - {r['nama_resep']}")

        resep_id = input("\nMasukkan ID resep (0 untuk kembali): ").strip()

        if resep_id == "0":
            return

        target = next((r for r in resep_list if str(r["id"]) == resep_id), None)
        if not target:
            Utils.print_error("ID resep tidak ditemukan!")
            Utils.pause_and_back()
            continue

        if not Utils.confirm_action(f"Hapus resep '{target['nama_resep']}'?"):
            Utils.print_warning("Dibatalkan.")
            Utils.pause_and_back()
            return

        result = RecipeService.hapus_resep(int(resep_id))

        if result["success"]:
            Utils.print_success(result["message"])
        else:
            Utils.print_error(result["message"])

        Utils.pause_and_back()
        return

def pulihkan_resep():
    from business.recovery_resep_service import RecipeRecoveryService
    from state import AppState

    while True:
        Utils.clear_screen()
        Utils.print_header("🔄 PULIHKAN RESEP")

        user_id = AppState.get_user_id()
        deleted = RecipeRecoveryService.get_deleted_recipes(user_id)

        if not deleted:
            Utils.print_warning("Tidak ada resep yang dapat dipulihkan.")
            Utils.pause_and_back()
            return

        print(f"\nDitemukan {len(deleted)} resep:\n")
        print("=" * 60)

        for i, r in enumerate(deleted, 1):
            print(f"{i}. {r['nama_resep'][:25]:<25} | Dihapus: {r['deleted_at']}")

        print("=" * 60)
        print("\nPilih nomor resep untuk dipulihkan")
        print("0. Kembali")

        choice = input("\nPilih: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice)
            if 1 <= idx <= len(deleted):
                resep = deleted[idx - 1]

                if not Utils.confirm_action(
                    f"Pulihkan resep '{resep['nama_resep']}'?"
                ):
                    Utils.print_warning("Dibatalkan.")
                    Utils.pause_and_back()
                    return

                result = RecipeRecoveryService.recover_recipe(resep["id"])

                if result["success"]:
                    Utils.print_success(result["message"])
                else:
                    Utils.print_error(result["message"])

                Utils.pause_and_back()
                return
            else:
                Utils.print_error("Pilihan tidak valid!")
                Utils.pause_and_back()

        except ValueError:
            Utils.print_error("Masukkan angka yang valid!")
            Utils.pause_and_back()
