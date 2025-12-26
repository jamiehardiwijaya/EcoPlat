from business.recipe_service import RecipeService
from utils.helper import Utils

def resep_menu():
    menu_items = [
        "➕ Tambah Resep",
        "📋 Lihat Resep Saya",
        "🌍 Lihat Semua Resep",
        "🗑️  Hapus Resep",
        "⬅️  Kembali"
    ]

    while True:
        Utils.clear_screen()
        Utils.print_header("MENU RESEP")

        for i, item in enumerate(menu_items, start=1):
            print(f"[{i}] {item}")

        pilihan = input("\nPilih menu [1-5]: ").strip()

        if pilihan == "1":
            tambah_resep()
        elif pilihan == "2":
            lihat_resep_saya()
        elif pilihan == "3":
            lihat_semua_resep()
        elif pilihan == "4":
            hapus_resep()
        elif pilihan == "5":
            return
        else:
            Utils.print_error("Pilihan tidak valid!")
            Utils.pause_and_back()

def tambah_resep():
    Utils.clear_screen()
    Utils.print_header("➕ TAMBAH RESEP")

    while True:
        nama = input("Nama resep      : ").strip()
        deskripsi = input("Deskripsi resep : ").strip()

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

def lihat_resep_saya():
    Utils.clear_screen()
    Utils.print_header("📋 RESEP SAYA")

    resep_list = RecipeService.lihat_resep_saya()

    if not resep_list:
        Utils.print_warning("Belum ada resep.")
        Utils.pause_and_back()
        return

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

    Utils.pause_and_back()

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

def hapus_resep():
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

        if not any(str(r["id"]) == resep_id for r in resep_list):
            Utils.print_error("ID resep tidak ditemukan!")
            Utils.pause_and_back()
            continue

        if not Utils.confirm_action("Yakin ingin menghapus resep ini?"):
            Utils.print_warning("Penghapusan dibatalkan.")
            Utils.pause_and_back()
            return

        result = RecipeService.hapus_resep(resep_id)

        if result["success"]:
            Utils.print_success(result["message"])
            Utils.pause_and_clear()
            return
        else:
            Utils.print_error(result["message"])
            Utils.pause_and_back()