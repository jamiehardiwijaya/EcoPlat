from business.recipe_service import RecipeService

def resep_menu():
    while True:
        print("\n" + "=" * 50)
        print("=== MENU RESEP ===")
        print("=" * 50)
        print("1. Tambah Resep")
        print("2. Lihat Resep Saya")
        print("3. Lihat Semua Resep")
        print("4. Hapus Resep")
        print("5. Kembali")

        pilihan = input("Pilih menu [1-5]: ").strip()

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
            print("Pilihan tidak valid!")

def tambah_resep():
    print("\n--- TAMBAH RESEP ---")
    nama = input("Nama resep: ").strip()
    deskripsi = input("Deskripsi resep: ").strip()

    print("\nMasukkan bahan (pisahkan dengan koma)")
    bahan_input = input("Contoh: telur,bawang,cabai : ").strip()

    daftar_bahan = [b.strip() for b in bahan_input.split(",") if b.strip()]

    result = RecipeService.tambah_resep(nama, deskripsi, daftar_bahan)
    print(result["message"])
    input("Tekan Enter untuk kembali...")

def lihat_resep_saya():
    print("\n--- RESEP SAYA ---")
    resep_list = RecipeService.lihat_resep_saya()

    if not resep_list:
        print("Belum ada resep.")
    else:
        for i, r in enumerate(resep_list, start=1):
            print(f"{i}. {r['nama_resep']}")
            print(f"   Deskripsi: {r['deskripsi']}\n")

    input("Tekan Enter untuk kembali...")

def lihat_semua_resep():
    print("\n--- SEMUA RESEP ---")
    resep_list = RecipeService.lihat_semua_resep()

    if not resep_list:
        print("Belum ada resep.")
    else:
        for i, r in enumerate(resep_list, start=1):
            print(f"{i}. {r['nama_resep']} (oleh {r['pembuat']})")
            print(f"   {r['deskripsi']}\n")

    input("Tekan Enter untuk kembali...")

def hapus_resep():
    resep_id = input("Masukkan ID resep yang akan dihapus: ").strip()

    result = RecipeService.hapus_resep(resep_id)
    print(result["message"])
    input("Tekan Enter untuk kembali...")