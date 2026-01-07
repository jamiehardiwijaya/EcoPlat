from business.history_service import HistoryService
from utils.helper import Utils
from datetime import datetime, timedelta

def get_status_icon(status):
    icon_map = {
        'ditambahkan': '➕',
        'dihapus': '🗑️',
        'digunakan': '🍳',
        'dikonsumsi': '🍽️',
        'kadaluarsa': '⚠️',
        'diupdate': '✏️',
        'terbuang': '🚮',
        'disimpan': '💾',
    }

    status_lower = status.lower()
    for key, icon in icon_map.items():
        if key in status_lower:
            return icon
    return '📝'

def get_status_description(status):
    descriptions = {
        'ditambahkan': 'Makanan ditambahkan ke inventaris',
        'dihapus': 'Makanan dihapus dari inventaris',
        'digunakan': 'Makanan digunakan untuk memasak',
        'dikonsumsi': 'Makanan langsung dimakan',
        'kadaluarsa': 'Makanan sudah lewat tanggal kadaluarsa',
        'diupdate': 'Informasi makanan diperbarui',
        'terbuang': 'Makanan terbuang karena tidak digunakan',
        'disimpan': 'Makanan disimpan dalam inventaris',
    }
    
    status_lower = status.lower()
    for key, desc in descriptions.items():
        if key in status_lower:
            return desc
    return 'Aktivitas lainnya'

def history_menu():
    while True:
        Utils.print_header("📜 Histori Aktivitas", show_user=False)
        
        menu = [
            "📋 Lihat Semua Histori",
            "📅 Lihat Histori Berdasarkan Periode",
            "🗑️ Lihat Makanan yang Terbuang",
            "🍳 Lihat Makanan yang Digunakan",
            "🔎 Cari Histori",
            "↩ Kembali ke Dashboard"
        ]
        
        choice = Utils.pilih_menu(menu)
        
        if choice == 1:
            lihat_semua_histori()
        elif choice == 2:
            lihat_histori_periode()
        elif choice == 3:
            lihat_makanan_terbuang()
        elif choice == 4:
            lihat_makanan_digunakan()
        elif choice == 5:
            cari_histori()
        elif choice == 6:
            return
        else:
            Utils.print_error("Pilihan tidak valid!")

def lihat_semua_histori():
    while True:
        Utils.print_header("📋 Semua Histori Aktivitas")
        histori = HistoryService.lihat_histori()
        
        if not histori:
            Utils.print_warning("Belum ada aktivitas yang tercatat.")
        else:
            print(f"📊 Total Aktivitas: {len(histori)}\n")
            print("═" * 100)
            print(f"{'No':<3} | {'Waktu':<19} | {'Aktivitas':<20} | {'Jumlah':<8} | {'Status':<30}")
            print("═" * 100)
            
            for i, aktivitas in enumerate(histori, start=1):
                waktu = aktivitas['timestamp'][:19] if 'timestamp' in aktivitas else aktivitas.get('timestamp', 'N/A')
                status_icon = get_status_icon(aktivitas['status'])
                status_desc = get_status_description(aktivitas['status'])
                nama = aktivitas['nama']
                if len(nama) > 18:
                    nama = nama[:15] + "..."
                
                print(f"{i:<3} | {waktu:<19} | {nama:<20} | "
                    f"{aktivitas['jumlah']:<8} | {status_icon} {status_desc}")
            
            print("═" * 100)
            
            if len(histori) > 0:
                print("\nℹ️  Masukkan nomor untuk melihat detail (0 untuk kembali)")
                while True:
                    pilih = input("Pilihan: ").strip()
                    if pilih == "0":
                        return
                    if not pilih:
                        Utils.print_error("Pilihan tidak boleh kosong")
                        continue
                    if pilih.isdigit() and 1 <= int(pilih) <= len(histori):
                        tampilkan_detail_histori(histori[int(pilih) - 1])
                        Utils.pause_and_clear()
                    else:
                        Utils.print_error("Pilihan tidak valid!")
                        continue
                    break

def lihat_histori_periode():
    while True:
        Utils.print_header("📅 Histori Berdasarkan Periode")
        
        print("Pilih periode:")
        print("1. Hari Ini")
        print("2. Kemarin")
        print("3. 7 Hari Terakhir")
        print("4. 30 Hari Terakhir")
        print("5. Custom Range")
        print("6. Kembali")
        pilihan = input("\nPilih [1-6]: ").strip()
            
        if pilihan == "6":
            return
            
        try:
            today = datetime.now().date()
                
            if pilihan == "1":
                start_date = end_date = today.strftime('%Y-%m-%d')
                label = "Hari Ini"
            elif pilihan == "2":
                start_date = end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
                label = "Kemarin"
            elif pilihan == "3":
                start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
                end_date = today.strftime('%Y-%m-%d')
                label = "7 Hari Terakhir"
            elif pilihan == "4":
                start_date = (today - timedelta(days=29)).strftime('%Y-%m-%d')
                end_date = today.strftime('%Y-%m-%d')
                label = "30 Hari Terakhir"
            elif pilihan == "5":
                print("\nFormat tanggal: YYYY-MM-DD")
                while True:
                    start_date = input("Tanggal mulai: ").strip()

                    if start_date == "0":
                        return
                    if not start_date:
                        Utils.print_error("Tanggal mulai tidak boleh kosong!")
                        continue
                    try:
                        datetime.strptime(start_date, '%Y-%m-%d')
                    except ValueError:
                        Utils.print_error("Format tanggal salah! Gunakan format YYYY-MM-DD. Contoh 2023-08-15")
                        continue
                    break

                while True:
                    end_date = input("Tanggal selesai: ").strip()

                    if end_date == "0":
                        return
                    if not end_date:
                        Utils.print_error("Tanggal selesai tidak boleh kosong!")
                        continue
                    try:
                        datetime.strptime(end_date, '%Y-%m-%d')
                    except ValueError:
                        Utils.print_error("Format tanggal salah! Gunakan format YYYY-MM-DD. Contoh 2023-08-15")
                        continue
                    break
                    
                label = f"{start_date} hingga {end_date}"
            else:
                Utils.print_error("Pilihan tidak valid!")
                Utils.pause_and_back()
                continue
                
            Utils.loading_animation(1, f"Mengambil data {label}")
                
            histori = HistoryService.lihat_histori_periode(start_date, end_date)
                
            if not histori:
                Utils.print_warning(f"Tidak ada aktivitas pada periode {label}")
                Utils.pause_and_clear()
                continue
            else:
                Utils.print_success(f"Ditemukan {len(histori)} aktivitas pada periode {label}\n")
                    
                while True:
                    print("═" * 90)
                    print(f"{'No':<3} | {'Waktu':<16} | {'Nama':<20} | {'Jumlah':<8} | {'Kategori':<12} | {'Status':<25}")
                    print("═" * 90)
                    
                    for i, aktivitas in enumerate(histori, start=1):
                        waktu = aktivitas['timestamp'][:16]
                        status_icon = get_status_icon(aktivitas['status'])
                        status_desc = get_status_description(aktivitas['status'])
                        
                        nama = aktivitas['nama']
                        if len(nama) > 18:
                            nama = nama[:15] + "..."
                        
                        status_display = f"{status_icon} {status_desc[:20]}"
                        
                        print(f"{i:<3} | {waktu:<16} | {nama:<20} | "
                            f"{aktivitas['jumlah']:<8} | {aktivitas['jenis_makanan'][:10]:<12} | {status_display:<25}")
                    
                    print("═" * 90)
                    
                    print("\nℹ️  Masukkan nomor untuk melihat detail (0 untuk kembali ke menu periode)")
                    pilih = input("Pilihan: ").strip()
                    
                    if pilih == "0":
                        break
                    elif not pilih:
                        Utils.print_error("Pilihan tidak boleh kosong")
                        Utils.pause_and_clear(1)
                        continue
                    elif pilih.isdigit() and 1 <= int(pilih) <= len(histori):
                        tampilkan_detail_histori(histori[int(pilih) - 1])
                        Utils.pause_and_clear(2)
                        continue
                    else:
                        Utils.print_error("Pilihan tidak valid!")
                        Utils.pause_and_clear(1)
                        continue
                    
        except ValueError:
            Utils.print_error("Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
            Utils.pause_and_clear()
        except Exception as e:
            Utils.print_error(f"Terjadi kesalahan: {e}")
            Utils.pause_and_clear()

def lihat_makanan_terbuang():
    Utils.print_header("🗑️ Makanan yang Terbuang")
    
    wasted_food = HistoryService.get_wasted_food_report()
    
    if not wasted_food:
        Utils.print_success("🎉 Tidak ada makanan yang terbuang!")
        print("Selamat! Anda berhasil menghindari food waste. 💚")
    else:
        print(f"⚠️  TOTAL MAKANAN TERBUANG: {len(wasted_food)}\n")
        print("Inilah makanan-makanan yang terbuang:")
        print("═" * 60)
        
        for i, makanan in enumerate(wasted_food, start=1):
            
            print(f"{i}. {makanan['nama']}")
            print(f"   Jumlah: {makanan['jumlah']} | Kategori: {makanan['jenis_makanan']}")
            if makanan.get('tanggal_kadaluwarsa'):
                print(f"   Kadaluarsa: {makanan['tanggal_kadaluwarsa']}")
            print(f"   Waktu: {makanan['timestamp'][:16]}")
            print()
        
        print("═" * 60)
        
        print(f"\n💡 TIPS MENGURANGI FOOD WASTE:")
        print("1. Periksa tanggal kadaluarsa secara berkala")
        print("2. Gunakan bahan yang hampir kadaluarsa terlebih dahulu")
        print("3. Beli bahan makanan sesuai kebutuhan")
        print("4. Simpan makanan dengan benar untuk memperpanjang umur simpan")
    
    Utils.pause_and_back()

def lihat_makanan_digunakan():
    Utils.print_header("🍳 Makanan yang Digunakan")
    
    histori = HistoryService.lihat_histori()
    used_food = [h for h in histori if h['status'] in ['digunakan', 'dikonsumsi']]
    
    if not used_food:
        Utils.print_warning("Belum ada makanan yang digunakan/dikonsumsi.")
    else:
        print(f"🍽️  TOTAL MAKANAN DIGUNAKAN: {len(used_food)}\n")
        
        grouped_by_day = {}
        for makanan in used_food:
            tanggal = makanan['timestamp'][:10]
            if tanggal not in grouped_by_day:
                grouped_by_day[tanggal] = []
            grouped_by_day[tanggal].append(makanan)
        
        dates_items = list(grouped_by_day.items())
        n_dates = len(dates_items)
        
        for i in range(n_dates):
            swapped = False
            for j in range(0, n_dates - i - 1):
                if dates_items[j][0] < dates_items[j + 1][0]:
                    dates_items[j], dates_items[j + 1] = dates_items[j + 1], dates_items[j]
                    swapped = True
            
            if not swapped:
                break
        
        for tanggal, items in dates_items:
            hari = datetime.strptime(tanggal, '%Y-%m-%d').strftime('%A, %d %B %Y')
            print(f"\n📅 {hari}")
            print("-" * 40)
            
            total_hari = sum(Utils.parse_jumlah(item['jumlah']) for item in items)
            print(f"Total item digunakan: {total_hari}")
            
            for item in items:
                status_icon = get_status_icon(item['status'])
                status_desc = get_status_description(item['status'])
                print(f"  {status_icon} {item['nama']} ({item['jumlah']} {item['jenis_makanan']})")
                print(f"    {status_desc}")
        
        total_item = sum(Utils.parse_jumlah(item['jumlah']) for item in used_food)
        print(f"\n📊 TOTAL SEMUA: {len(used_food)} aktivitas, {total_item} item")
        
        print(f"\n💡 REKOMENDASI:")
        print("• Terus catat penggunaan makanan untuk analisis pola konsumsi")
        print("• Bandingkan dengan jumlah makanan terbuang untuk evaluasi")
    
    Utils.pause_and_back()

def cari_histori():
    while True:
        Utils.print_header("🔎 Cari Histori")
        print("Ketik 0 untuk kembali ke menu sebelumnya.\n")
        print("Cari berdasarkan: nama, status, atau kategori makanan")
        print("Contoh: 'nasi', 'digunakan', 'sayuran', 'ditambahkan'")
        print("-" * 60)
        
        keyword = input("Masukkan kata kunci pencarian (*berdasarkan nama, status, kategori): ").strip()
        if keyword == "0":
            return
        
        if not keyword:
            Utils.print_error("Kata kunci tidak boleh kosong!")
            continue
        
        if keyword.lower() in ['kembali', 'batal', 'exit', 'keluar']:
            break
        
        Utils.loading_animation(1, f"Mencari '{keyword}'")
        
        results = HistoryService.search_history(keyword)
        
        if not results:
            Utils.print_warning(f"Tidak ditemukan hasil untuk '{keyword}'")
            Utils.pause_and_clear()
            continue
        
        Utils.print_success(f"Ditemukan {len(results)} hasil untuk '{keyword}'\n")
        
        while True:
            print("═" * 90)
            print(f"{'No':<3} | {'Waktu':<16} | {'Nama':<20} | {'Jumlah':<8} | {'Kategori':<12} | {'Status':<25}")
            print("═" * 90)
            
            for i, result in enumerate(results, start=1):
                waktu = result['timestamp'][:16]
                status_icon = get_status_icon(result['status'])
                status_desc = get_status_description(result['status'])
                
                nama = result['nama']
                if len(nama) > 18:
                    nama = nama[:15] + "..."
                
                status_display = f"{status_icon} {status_desc[:20]}"
                
                print(f"{i:<3} | {waktu:<16} | {nama:<20} | "
                    f"{result['jumlah']:<8} | {result['jenis_makanan'][:10]:<12} | {status_display:<25}")
            
            if len(results) > 20:
                print(f"... dan {len(results) - 20} hasil lainnya")
            
            print("═" * 90)
            
            print("\nℹ️  Pilihan:")
            print("1. Lihat detail histori (masukkan nomor)")
            print("2. Cari lagi")
            print("0. Kembali ke menu Histori")
            
            pilihan = input("\nPilih [1/2/0] atau masukkan nomor histori: ").strip()
            
            if pilihan == "0":
                return
            elif pilihan == "1" or pilihan.isdigit() and 1 <= int(pilihan) <= len(results):
                if pilihan == "1":
                    while True:
                        nomor = input("Masukkan nomor histori: ").strip()
                        if nomor.isdigit() and 1 <= int(nomor) <= len(results):
                            tampilkan_detail_histori(results[int(nomor) - 1])
                            Utils.pause_and_clear(2)
                            break
                        elif nomor == "0":
                            break
                        else:
                            Utils.print_error("Nomor tidak valid!")
                else:
                    tampilkan_detail_histori(results[int(pilihan) - 1])
                    Utils.pause_and_clear(2)
                continue
            elif pilihan == "2":
                break
            else:
                Utils.print_error("Pilihan tidak valid!")
                Utils.pause_and_clear(1)
                continue

def tampilkan_detail_histori(aktivitas):
    Utils.print_header("📄 Detail Histori")
    
    print(f"\n📋 INFORMASI AKTIVITAS")
    print("═" * 50)
    print(f"Nama Makanan     : {aktivitas['nama']}")
    print(f"Jumlah           : {aktivitas['jumlah']}")
    print(f"Kategori         : {aktivitas['jenis_makanan']}")
    status_icon = get_status_icon(aktivitas['status'])
    status_desc = get_status_description(aktivitas['status'])
    print(f"Status           : {status_icon} {status_desc}")
    
    if 'tanggal_kadaluwarsa' in aktivitas and aktivitas['tanggal_kadaluwarsa']:
        print(f"Tanggal Kadaluarsa: {aktivitas['tanggal_kadaluwarsa']}")
    
    print(f"\n⏰ WAKTU")
    print("═" * 50)
    waktu = datetime.strptime(aktivitas['timestamp'], '%Y-%m-%d %H:%M:%S')
    print(f"Tanggal      : {waktu.strftime('%A, %d %B %Y')}")
    print(f"Waktu        : {waktu.strftime('%H:%M:%S')}")
    print(f"Durasi       : {calculate_time_ago(waktu)}")
    
    print(f"\n📍 INFORMASI TAMBAHAN")
    print("═" * 50)
    if 'sisa_makanan_id' in aktivitas and aktivitas['sisa_makanan_id']:
        print(f"ID Makanan    : {aktivitas['sisa_makanan_id']}")
    
    status_msg = get_status_message(aktivitas['status'])
    if status_msg:
        print(f"\n💭 PESAN:")
        print(f"  {status_msg}")

def calculate_time_ago(timestamp):
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} tahun yang lalu"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} bulan yang lalu"
    elif diff.days > 0:
        return f"{diff.days} hari yang lalu"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} jam yang lalu"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} menit yang lalu"
    else:
        return f"{diff.seconds} detik yang lalu"

def get_status_message(status):
    messages = {
        'ditambahkan': 'Makanan baru ditambahkan ke inventaris.',
        'dihapus': 'Makanan dihapus dari inventaris.',
        'digunakan': 'Makanan digunakan untuk memasak/membuat sesuatu.',
        'dikonsumsi': 'Makanan langsung dikonsumsi.',
        'kadaluarsa': 'Makanan telah melewati tanggal kadaluarsa.',
        'terbuang': 'Makanan terbuang sia-sia karena tidak digunakan sebelum kadaluarsa.',
        'diupdate': 'Informasi makanan diperbarui.',
    }
    
    status_lower = status.lower()
    for key, message in messages.items():
        if key in status_lower:
            return message
    
    return ""