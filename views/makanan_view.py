from business.food_service import FoodService
from utils.helper import Utils
from datetime import datetime


def makanan_menu():
    menu_items = [
        "➕ Tambah Makanan",
        "📋 Lihat Daftar Makanan",
        "✏️  Update Makanan",
        "🗑️  Hapus Makanan",
        "🔄 Pulihkan Makanan",  # Menu baru untuk pemulihan
        "⬅️  Kembali"
    ]

    while True:
        Utils.clear_screen()
        Utils.print_header("MENU MAKANAN")

        for i, item in enumerate(menu_items, start=1):
            print(f"[{i}] {item}")

        pilihan = input("\nPilih menu [1-6]: ").strip()

        if pilihan == "1":
            tambah_makanan()
        elif pilihan == "2":
            lihat_makanan()
        elif pilihan == "3":
            update_makanan()
        elif pilihan == "4":
            hapus_makanan()
        elif pilihan == "5":  # Menu pemulihan
            pulihkan_makanan()
        elif pilihan == "6":
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
        while True:
            tanggal = input(f"Tanggal [{target['tanggal_kadaluarsa']}]: ").strip() or target["tanggal_kadaluarsa"]
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
        
        print(f"\n💡 Informasi:")
        print(f"• Makanan akan dicatat di histori")
        print(f"• Dapat dipulihkan nanti melalui menu '🔄 Pulihkan Makanan'")
        print(f"• Data akan disimpan selama 30 hari")

        if not Utils.confirm_action("Yakin ingin menghapus makanan ini?"):
            Utils.print_warning("Penghapusan dibatalkan.")
            Utils.pause_and_back()
            return

        result = FoodService.hapus_makanan(id_makanan)

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
    from business.recovery_service import RecoveryService
    from state import AppState
    
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
            print("\n1. Kembali ke Menu Makanan")
            choice = input("\nPilih: ").strip()
            if choice == "1":
                return
            continue

        stats = RecoveryService.get_waste_reduction_stats()
        print(f"\n📊 STATISTIK PEMULIHAN:")
        print(f"   • Total dihapus       : {stats['total_deleted']}")
        print(f"   • Berhasil dipulihkan : {stats['total_recovered']}")
        print(f"   • Tingkat pemulihan   : {stats['recovery_rate']:.1f}%")
        print(f"   • Food waste dicegah  : {stats['waste_prevented']} item")
        
        print(f"\n📋 MAKANAN YANG DAPAT DIPULIHKAN: {len(deleted_foods)} item\n")
        
        print("═" * 70)
        for i, food in enumerate(deleted_foods[:10], 1): 
            try:
                deleted_time = datetime.strptime(food['deleted_at'], '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                diff = now - deleted_time
                
                if diff.days > 0:
                    time_ago = f"{diff.days} hari lalu"
                elif diff.seconds > 3600:
                    time_ago = f"{diff.seconds // 3600} jam lalu"
                elif diff.seconds > 60:
                    time_ago = f"{diff.seconds // 60} menit lalu"
                else:
                    time_ago = f"{diff.seconds} detik lalu"
                
                print(f"{i}. {food['nama_makanan']}")
                print(f"   Jumlah: {food['jumlah']} | Kategori: {food['kategori']}")
                print(f"   Kadaluarsa: {food['tanggal_kadaluarsa']}")
                print(f"   Dihapus: {time_ago} | Status: {food['status_deletion']}")
                print()
            except Exception as e:
                print(f"{i}. {food.get('nama_makanan', 'Unknown')} [Error: {e}]")
                print()
        
        if len(deleted_foods) > 10:
            print(f"... dan {len(deleted_foods) - 10} makanan lainnya")
        print("═" * 70)
        
        print("\n📋 MENU:")
        print("1-9. Pilih nomor untuk memulihkan")
        print("10.  Tampilkan semua makanan")
        print("11.  Hapus permanen makanan terpilih")
        print("12.  Lihat statistik lengkap")
        print("13.  Kembali ke Menu Makanan")
        
        choice = input("\n🎯 Pilih [1-13]: ").strip()
        
        try:
            if choice.isdigit():
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(deleted_foods[:10]):
                    food_to_recover = deleted_foods[choice_num - 1]
                    
                    Utils.clear_screen()
                    Utils.print_header("🔍 DETAIL MAKANAN UNTUK DIPULIHKAN")
                    
                    print(f"\n📋 INFORMASI MAKANAN:")
                    print("═" * 50)
                    print(f"Nama       : {food_to_recover['nama_makanan']}")
                    print(f"Jumlah     : {food_to_recover['jumlah']}")
                    print(f"Kategori   : {food_to_recover['kategori']}")
                    print(f"Kadaluarsa : {food_to_recover['tanggal_kadaluarsa']}")
                    print(f"Dihapus    : {food_to_recover['deleted_at'][:16]}")
                    print(f"Status     : {food_to_recover['status_deletion']}")
                    print("═" * 50)
                    
                    print(f"\n💡 KETERANGAN:")
                    if food_to_recover['status_deletion'] == 'terbuang':
                        print("• Makanan ini dicatat sebagai TERBUANG karena sudah kadaluarsa.")
                        print("• Jika dipulihkan, akan dikembalikan ke inventaris.")
                    elif food_to_recover['status_deletion'] == 'digunakan':
                        print("• Makanan ini dicatat sebagai DIGUNAKAN sebelum kadaluarsa.")
                        print("• Jika dipulihkan, akan dikembalikan ke inventaris.")
                    else:
                        print("• Makanan ini dihapus tanpa status khusus.")
                        print("• Jika dipulihkan, akan dikembalikan ke inventaris.")
                    
                    confirm = input(f"\n✅ Pulihkan '{food_to_recover['nama_makanan']}'? (y/n): ").lower()
                    if confirm == 'y':
                        result = RecoveryService.recover_food(food_to_recover['id'])
                        
                        if result["success"]:
                            Utils.print_success(result["message"])
                            print(f"\n📝 Makanan berhasil dikembalikan ke daftar makanan Anda.")
                            print(f"   Cek di menu 'Lihat Daftar Makanan' untuk melihatnya.")
                        else:
                            Utils.print_error(result["message"])
                        
                        Utils.pause_and_back()
                        return
                    else:
                        Utils.print_warning("Pemulihan dibatalkan.")
                        Utils.pause_and_back()
                
                elif choice_num == 10:
                    Utils.clear_screen()
                    Utils.print_header("📋 SEMUA MAKANAN YANG DIHAPUS")
                    
                    print(f"Total: {len(deleted_foods)} makanan\n")
                    print("═" * 80)
                    
                    for i, food in enumerate(deleted_foods, 1):
                        try:
                            deleted_time = datetime.strptime(food['deleted_at'], '%Y-%m-%d %H:%M:%S')
                            formatted_time = deleted_time.strftime('%d/%m %H:%M')
                            
                            print(f"{i:>3}. {food['nama_makanan']:<20} | "
                                  f"Jml: {food['jumlah']:>3} | "
                                  f"Kat: {food['kategori']:<10} | "
                                  f"Exp: {food['tanggal_kadaluarsa']} | "
                                  f"Hapus: {formatted_time}")
                        except:
                            print(f"{i:>3}. {food.get('nama_makanan', 'Unknown')}")
                    
                    print("═" * 80)
                    print("\nMasukkan nomor untuk memulihkan (0 untuk kembali)")
                    food_choice = input("Pilih: ").strip()
                    
                    if food_choice.isdigit():
                        food_num = int(food_choice)
                        if 1 <= food_num <= len(deleted_foods):
                            selected_food = deleted_foods[food_num - 1]
                            confirm = input(f"Pulihkan '{selected_food['nama_makanan']}'? (y/n): ").lower()
                            if confirm == 'y':
                                result = RecoveryService.recover_food(selected_food['id'])
                                if result["success"]:
                                    Utils.print_success(result["message"])
                                else:
                                    Utils.print_error(result["message"])
                                Utils.pause_and_back()
                                return
                    
                    Utils.pause_and_back()
                
                elif choice_num == 11:
                    Utils.clear_screen()
                    Utils.print_header("🗑️ HAPUS PERMANEN MAKANAN")
                    
                    print("Pilih makanan yang akan dihapus permanen:")
                    print("═" * 50)
                    
                    for i, food in enumerate(deleted_foods[:5], 1):
                        print(f"{i}. {food['nama_makanan']} ({food['jumlah']} pcs)")
                    
                    print("═" * 50)
                    print("\nMasukkan nomor (0 untuk batal)")
                    delete_choice = input("Pilih: ").strip()
                    
                    if delete_choice.isdigit():
                        delete_num = int(delete_choice)
                        if 1 <= delete_num <= len(deleted_foods[:5]):
                            food_to_delete = deleted_foods[delete_num - 1]
                            confirm = input(f"\n❌ HAPUS PERMANEN '{food_to_delete['nama_makanan']}'? (y/n): ").lower()
                            if confirm == 'y':
                                result = RecoveryService.permanently_delete_from_csv(food_to_delete['id'])
                                if result["success"]:
                                    Utils.print_success(result["message"])
                                else:
                                    Utils.print_error(result["message"])
                                Utils.pause_and_back()
                                return
                    
                    Utils.print_warning("Penghapusan dibatalkan.")
                    Utils.pause_and_back()
                
                elif choice_num == 12:
                    show_recovery_statistics()
                
                elif choice_num == 13:
                    return
        
        except ValueError:
            Utils.print_error("Masukkan angka yang valid!")
            Utils.pause_and_back()
        except Exception as e:
            Utils.print_error(f"Terjadi kesalahan: {e}")
            Utils.pause_and_back()

def show_recovery_statistics():
    """Menampilkan statistik pemulihan lengkap"""
    from business.recovery_service import RecoveryService
    from state import AppState
    
    Utils.clear_screen()
    Utils.print_header("📈 STATISTIK PEMULIHAN LENGKAP")
    
    stats = RecoveryService.get_waste_reduction_stats()
    user_id = AppState.get_user_id()
    
    print(f"\n📊 STATISTIK UMUM:")
    print("═" * 50)
    print(f"• Total makanan dihapus      : {stats['total_deleted']}")
    print(f"• Berhasil dipulihkan        : {stats['total_recovered']}")
    print(f"• Belum dipulihkan           : {stats['total_deleted'] - stats['total_recovered']}")
    print(f"• Tingkat keberhasilan       : {stats['recovery_rate']:.1f}%")
    print(f"• Food waste dicegah         : {stats['waste_prevented']} item")
    
    if stats['total_deleted'] > 0:
        efficiency = stats['recovery_rate']
        if efficiency > 70:
            rating = "🎉 EXCELLENT"
            color = "🟢"
        elif efficiency > 50:
            rating = "👍 BAIK"
            color = "🟡"
        elif efficiency > 30:
            rating = "⚠️  SEDANG"
            color = "🟠"
        else:
            rating = "❌ PERLU PERBAIKAN"
            color = "🔴"
        
        print(f"\n🏆 PENILAIAN EFISIENSI: {color} {rating}")
    
    deleted_foods = RecoveryService.get_deleted_foods(user_id)
    all_deleted_foods = []
    print(f"\n🏷️  ANALISIS KATEGORI:")
    print("═" * 50)
    
    category_counts = {}
    for food in deleted_foods:
        kategori = food.get('kategori', 'Tidak Diketahui')
        if kategori not in category_counts:
            category_counts[kategori] = 0
        category_counts[kategori] += 1
    
    if category_counts:
        for kategori, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"• {kategori}: {count} makanan")
    else:
        print("• Tidak ada data kategori")
    
    print(f"\n💡 REKOMENDASI:")
    print("═" * 50)
    
    if stats['recovery_rate'] < 30:
        print("• ⚠️  Tingkat pemulihan rendah (<30%).")
        print("• 🕒 Beri waktu 1-2 hari sebelum menghapus permanen")
        print("• 📋 Periksa makanan sebelum menghapus")
        print("• 🔔 Gunakan fitur 'Hampir Kadaluarsa' untuk peringatan dini")
    elif stats['recovery_rate'] < 70:
        print("• 👍 Tingkat pemulihan cukup baik.")
        print("• 📊 Pertahankan kebiasaan memulihkan makanan")
        print("• 🗓️  Jadwalkan pemulihan setiap minggu")
        print("• 🔄 Prioritaskan makanan yang baru dihapus")
    else:
        print("• 🎉 Tingkat pemulihan sangat baik! 💚")
        print("• 💪 Anda telah mencegah banyak food waste!")
        print("• 📚 Bagikan tips Anda ke pengguna lain")
    
    print("\n🎯 TIPS UMUM:")
    print("• Gunakan fitur 'Hampir Kadaluarsa' untuk peringatan dini")
    print("• Rencanakan menu mingguan untuk mengurangi pembelian berlebihan")
    print("• Simpan makanan dengan benar untuk memperpanjang umur simpan")
    print("• Periksa inventaris sebelum berbelanja")
    
    Utils.pause_and_back()