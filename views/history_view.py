from business.history_service import HistoryService
from utils.helper import Utils
from datetime import datetime, timedelta

def get_status_icon(status):
    """
    Mengembalikan icon berdasarkan status aktivitas
    """
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

def history_menu():
    """Menu utama histori"""
    while True:
        Utils.print_header("📜 Histori Aktivitas", show_user=False)
        
        menu = [
            "📋 Lihat Semua Histori",
            "📅 Lihat Histori Berdasarkan Periode",
            "📊 Statistik & Analisis Lengkap",
            "🔍 Aktivitas Terbaru",
            "🗑️ Lihat Makanan yang Terbuang",
            "🍳 Lihat Makanan yang Digunakan",
            "🔎 Cari Histori",
            "📈 Ringkasan Bulanan",
            "↩ Kembali ke Dashboard"
        ]
        
        choice = Utils.pilih_menu(menu)
        
        if choice == 1:
            lihat_semua_histori()
        elif choice == 2:
            lihat_histori_periode()
        elif choice == 3:
            lihat_statistik_lengkap()
        elif choice == 4:
            lihat_aktivitas_terbaru()
        elif choice == 5:
            lihat_makanan_terbuang()
        elif choice == 6:
            lihat_makanan_digunakan()
        elif choice == 7:
            cari_histori()
        elif choice == 8:
            lihat_ringkasan_bulanan()
        elif choice == 9:
            return
        else:
            Utils.print_error("Pilihan tidak valid!")

def lihat_semua_histori():
    """Menampilkan semua histori aktivitas"""
    Utils.print_header("📋 Semua Histori Aktivitas")
    
    histori = HistoryService.lihat_histori()
    
    if not histori:
        Utils.print_warning("Belum ada aktivitas yang tercatat.")
    else:
        print(f"📊 Total Aktivitas: {len(histori)}\n")
        print("═" * 80)
        print(f"{'No':<3} | {'Waktu':<19} | {'Aktivitas':<20} | {'Jumlah':<8} | {'Status':<12}")
        print("═" * 80)
        
        for i, aktivitas in enumerate(histori, start=1):
            waktu = aktivitas['timestamp'][:19] if 'timestamp' in aktivitas else aktivitas.get('timestamp', 'N/A')
            status_icon = get_status_icon(aktivitas['status'])
            nama = aktivitas['nama']
            if len(nama) > 18:
                nama = nama[:15] + "..."
            
            print(f"{i:<3} | {waktu:<19} | {nama:<20} | "
                  f"{aktivitas['jumlah']:<8} | {status_icon:<12}")
        
        print("═" * 80)
        
        if len(histori) > 0:
            print("\nℹ️  Masukkan nomor untuk melihat detail (0 untuk kembali)")
            pilih = input("Pilihan: ").strip()
            
            if pilih.isdigit() and 1 <= int(pilih) <= len(histori):
                tampilkan_detail_histori(histori[int(pilih) - 1])
    
    Utils.pause_and_back()

def lihat_histori_periode():
    """Menampilkan histori berdasarkan periode"""
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
            start_date = input("Tanggal mulai: ").strip()
            end_date = input("Tanggal selesai: ").strip()
            
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            
            label = f"{start_date} hingga {end_date}"
        else:
            Utils.print_error("Pilihan tidak valid!")
            Utils.pause_and_back()
            return
        
        Utils.loading_animation(1, f"Mengambil data {label}")
        
        histori = HistoryService.lihat_histori_periode(start_date, end_date)
        
        if not histori:
            Utils.print_warning(f"Tidak ada aktivitas pada periode {label}")
        else:
            Utils.print_success(f"Ditemukan {len(histori)} aktivitas pada periode {label}\n")
            
            print("═" * 70)
            for i, aktivitas in enumerate(histori[:20], start=1):  
                waktu = aktivitas['timestamp'][11:16]  
                status_icon = get_status_icon(aktivitas['status'])
                
                print(f"{i:>2}. [{waktu}] {status_icon} {aktivitas['nama']} "
                      f"({aktivitas['jumlah']} {aktivitas['jenis_makanan']})")
            
            if len(histori) > 20:
                print(f"\n... dan {len(histori) - 20} aktivitas lainnya")
            
            print("═" * 70)
            
    except ValueError:
        Utils.print_error("Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
    except Exception as e:
        Utils.print_error(f"Terjadi kesalahan: {e}")
    
    Utils.pause_and_back()

def calculate_efficiency_stats(statistik):
    """Menghitung statistik efisiensi"""
    if not statistik.get("detail"):
        return {"persentase_digunakan": 0, "persentase_terbuang": 0}
    
    total_items = statistik.get("total_item", 0)
    if total_items == 0:
        return {"persentase_digunakan": 0, "persentase_terbuang": 0}
    
    used_items = 0
    for status in ['digunakan', 'dikonsumsi']:
        if status in statistik["detail"]:
            used_items += statistik["detail"][status].get("total_item", 0)
    
    wasted_items = 0
    for status in ['terbuang', 'kadaluarsa']:
        if status in statistik["detail"]:
            wasted_items += statistik["detail"][status].get("total_item", 0)
    
    return {
        "persentase_digunakan": (used_items / total_items) * 100,
        "persentase_terbuang": (wasted_items / total_items) * 100,
        "used_items": used_items,
        "wasted_items": wasted_items
    }

def lihat_statistik_lengkap():
    """Menampilkan statistik histori lengkap"""
    Utils.print_header("📊 Statistik & Analisis Histori")
    
    Utils.loading_animation(1.5, "Menganalisis data")
    
    statistik = HistoryService.get_statistik_histori()
    
    if not statistik.get("detail"):
        Utils.print_warning("Belum ada data statistik.")
    else:
        print(f"\n📈 OVERVIEW STATISTIK")
        print("═" * 50)
        print(f"Total Aktivitas  : {statistik['total_aktivitas']}")
        print(f"Total Item       : {statistik['total_item']}")
        print(f"Aktivitas Hari Ini : {statistik['ringkasan'].get('hari_ini', 0)}")
        print(f"Aktivitas Kemarin  : {statistik['ringkasan'].get('kemarin', 0)}")
        
        print(f"\n📋 DETAIL PER STATUS")
        print("═" * 50)
        
        status_items = list(statistik['detail'].items())
        n = len(status_items)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if status_items[j][1]['jumlah_aktivitas'] < status_items[j + 1][1]['jumlah_aktivitas']:
                    status_items[j], status_items[j + 1] = status_items[j + 1], status_items[j]
                    swapped = True
            
            if not swapped:
                break

        for status, data in status_items:
            status_icon = get_status_icon(status)
            persentase = (data['jumlah_aktivitas'] / statistik['total_aktivitas'] * 100) if statistik['total_aktivitas'] > 0 else 0
            
            print(f"\n{status_icon} {status.upper()}:")
            print(f"  └ Jumlah Aktivitas : {data['jumlah_aktivitas']}")
            print(f"  └ Total Item       : {data['total_item']}")
            print(f"  └ Persentase       : {persentase:.1f}%")
            
            if data.get('by_category'):
                print(f"  └ Kategori:")
                kategori_items = list(data['by_category'].items())
                k_n = len(kategori_items)
                
                for k in range(k_n):
                    swapped_k = False
                    for l in range(0, k_n - k - 1):
                        if kategori_items[l][1] < kategori_items[l + 1][1]:
                            kategori_items[l], kategori_items[l + 1] = kategori_items[l + 1], kategori_items[l]
                            swapped_k = True
                    if not swapped_k:
                        break
                
                for kategori, jumlah in kategori_items:
                    print(f"    • {kategori}: {jumlah} item")
        
        print(f"\n🔍 ANALISIS LANJUT")
        print("═" * 50)
        
        efficiency_stats = calculate_efficiency_stats(statistik)
        
        print(f"🍽️  Makanan Digunakan   : {statistik['analisis'].get('total_digunakan', 0)} aktivitas")
        print(f"🗑️  Makanan Terbuang     : {statistik['analisis'].get('total_terbuang', 0)} aktivitas")
        print(f"📦 Total Item Digunakan : {efficiency_stats['used_items']} item")
        print(f"🗑️  Total Item Terbuang  : {efficiency_stats['wasted_items']} item")
        
        if statistik['total_item'] > 0:
            print(f"✅ Efisiensi Penggunaan : {efficiency_stats['persentase_digunakan']:.1f}%")
            print(f"⚠️  Tingkat Pemborosan   : {efficiency_stats['persentase_terbuang']:.1f}%")
        
        print(f"\n💡 REKOMENDASI")
        print("═" * 50)
        
        total_terbuang = efficiency_stats['wasted_items']
        total_semua = statistik['total_item']
        
        if total_semua > 0:
            persentase_terbuang = (total_terbuang / total_semua) * 100
            
            if persentase_terbuang > 20:
                print("• ⚠️  Tingkat pemborosan tinggi (>20%). Perhatikan tanggal kadaluarsa!")
                print("• 🍳 Gunakan fitur 'Rekomendasi Resep' untuk bahan hampir kadaluarsa")
                print("• 📅 Setel pengingat untuk memeriksa makanan secara berkala")
            elif persentase_terbuang > 5:
                print("• 👍 Tingkat pemborosan sedang. Bisa ditingkatkan!")
                print("• 🗓️  Rencanakan menu mingguan untuk mengurangi pemborosan")
            else:
                print("• 🎉 Tingkat pemborosan rendah. Pertahankan! 💚")
                print("• 📊 Lanjutkan pencatatan untuk menjaga konsistensi")
        else:
            print("• 🎉 Tidak ada makanan terbuang! Excellent!")
            print("• 💪 Pertahankan kebiasaan baik ini")
        
        print("• 📱 Gunakan notifikasi untuk pengingat kadaluarsa")
        print("• 🛒 Beli bahan sesuai kebutuhan, hindari penimbunan")
    
    Utils.pause_and_back()

def lihat_aktivitas_terbaru():
    """Menampilkan 10 aktivitas terbaru"""
    Utils.print_header("🔍 Aktivitas Terbaru")
    
    histori = HistoryService.lihat_histori(limit=10)
    
    if not histori:
        Utils.print_warning("Belum ada aktivitas yang tercatat.")
    else:
        print(f"🎯 10 AKTIVITAS TERBARU\n")
        print("═" * 70)
        
        for i, aktivitas in enumerate(histori, start=1):
            waktu_full = aktivitas['timestamp']
            waktu = datetime.strptime(waktu_full, '%Y-%m-%d %H:%M:%S')
            
            hari_ini = datetime.now().date()
            if waktu.date() == hari_ini:
                waktu_display = f"Hari ini {waktu.strftime('%H:%M')}"
            elif waktu.date() == hari_ini - timedelta(days=1):
                waktu_display = f"Kemarin {waktu.strftime('%H:%M')}"
            else:
                waktu_display = waktu.strftime('%d/%m %H:%M')
            
            status_icon = get_status_icon(aktivitas['status'])
            
            print(f"{i:>2}. {status_icon} [{waktu_display}]")
            print(f"    {aktivitas['nama']} - {aktivitas['jumlah']} {aktivitas['jenis_makanan']}")
            print()
        
        print("═" * 70)
    
    Utils.pause_and_back()

def lihat_makanan_terbuang():
    """Menampilkan makanan yang terbuang"""
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
    """Menampilkan makanan yang digunakan"""
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
            
            total_hari = sum(item['jumlah'] for item in items)
            print(f"Total item digunakan: {total_hari}")
            
            for item in items:
                status_icon = get_status_icon(item['status'])
                print(f"  {status_icon} {item['nama']} ({item['jumlah']} {item['jenis_makanan']})")
        
        total_item = sum(item['jumlah'] for item in used_food)
        print(f"\n📊 TOTAL SEMUA: {len(used_food)} aktivitas, {total_item} item")
        
        print(f"\n💡 REKOMENDASI:")
        print("• Terus catat penggunaan makanan untuk analisis pola konsumsi")
        print("• Bandingkan dengan jumlah makanan terbuang untuk evaluasi")
    
    Utils.pause_and_back()

def cari_histori():
    """Mencari histori berdasarkan keyword"""
    Utils.print_header("🔎 Cari Histori")
    
    keyword = input("Masukkan kata kunci pencarian: ").strip()
    
    if not keyword:
        Utils.print_error("Kata kunci tidak boleh kosong!")
        Utils.pause_and_back()
        return
    
    Utils.loading_animation(1, f"Mencari '{keyword}'")
    
    results = HistoryService.search_history(keyword)
    
    if not results:
        Utils.print_warning(f"Tidak ditemukan hasil untuk '{keyword}'")
    else:
        Utils.print_success(f"Ditemukan {len(results)} hasil untuk '{keyword}'\n")
        
        print("═" * 70)
        for i, result in enumerate(results[:15], start=1): 
            waktu = result['timestamp'][:16]
            status_icon = get_status_icon(result['status'])
            
            nama = result['nama']
            if keyword.lower() in nama.lower():
                nama = nama.replace(keyword, keyword.upper())
            
            print(f"{i:>2}. [{waktu}] {status_icon} {nama}")
            print(f"    Jumlah: {result['jumlah']} | Status: {result['status']} | "
                  f"Kategori: {result['jenis_makanan']}")
            print()
        
        if len(results) > 15:
            print(f"... dan {len(results) - 15} hasil lainnya")
        
        print("═" * 70)
    
    Utils.pause_and_back()

def lihat_ringkasan_bulanan():
    """Menampilkan ringkasan bulanan"""
    Utils.print_header("📈 Ringkasan Bulanan")
    
    print("Pilih bulan (format: YYYY-MM):")
    bulan_sekarang = datetime.now().strftime('%Y-%m')
    print(f"1. Bulan ini ({bulan_sekarang})")
    print("2. Bulan sebelumnya")
    print("3. Custom bulan")
    print("4. Kembali")
    
    pilihan = input("\nPilih [1-4]: ").strip()
    
    if pilihan == "4":
        return
    
    if pilihan == "1":
        year_month = bulan_sekarang
        label = "Bulan Ini"
    elif pilihan == "2":
        last_month = datetime.now() - timedelta(days=30)
        year_month = last_month.strftime('%Y-%m')
        label = "Bulan Sebelumnya"
    elif pilihan == "3":
        year_month = input("Masukkan tahun-bulan (YYYY-MM): ").strip()
        
        try:
            datetime.strptime(year_month + "-01", '%Y-%m-%d')
            label = f"Bulan {datetime.strptime(year_month + '-01', '%Y-%m-%d').strftime('%B %Y')}"
        except ValueError:
            Utils.print_error("Format tidak valid! Gunakan YYYY-MM")
            Utils.pause_and_back()
            return
    else:
        Utils.print_error("Pilihan tidak valid!")
        Utils.pause_and_back()
        return
    
    Utils.loading_animation(1, f"Menganalisis data {label}")
    
    summary = HistoryService.get_monthly_summary(year_month)
    
    if not summary:
        Utils.print_warning(f"Tidak ada data untuk {label}")
    else:
        print(f"\n📊 RINGKASAN {label.upper()}")
        print("═" * 60)
        
        grouped_by_date = {}
        for item in summary:
            tanggal = item['tanggal']
            if tanggal not in grouped_by_date:
                grouped_by_date[tanggal] = []
            grouped_by_date[tanggal].append(item)
        
        total_aktivitas = 0
        total_item = 0
        
        dates_items = list(grouped_by_date.items())
        n_dates = len(dates_items)
        
        for i in range(n_dates):
            swapped = False
            for j in range(0, n_dates - i - 1):
                if dates_items[j][0] > dates_items[j + 1][0]:
                    dates_items[j], dates_items[j + 1] = dates_items[j + 1], dates_items[j]
                    swapped = True
            
            if not swapped:
                break
        
        for tanggal, items in dates_items:
            hari = datetime.strptime(tanggal, '%Y-%m-%d').strftime('%a, %d')
            print(f"\n📅 {hari}")
            
            aktivitas_hari = sum(item['jumlah_aktivitas'] for item in items)
            item_hari = sum(item['total_item'] for item in items)
            
            total_aktivitas += aktivitas_hari
            total_item += item_hari
            
            print(f"  Aktivitas: {aktivitas_hari} | Item: {item_hari}")
            
            for item in items:
                status_icon = get_status_icon(item['status'])
                print(f"    {status_icon} {item['status']}: {item['total_item']} item")
        
        print("\n" + "═" * 60)
        print(f"📈 TOTAL BULAN INI:")
        print(f"  • Aktivitas: {total_aktivitas}")
        print(f"  • Item     : {total_item}")
        
        hari_kerja = len(grouped_by_date)
        if hari_kerja > 0:
            rata_aktivitas = total_aktivitas / hari_kerja
            rata_item = total_item / hari_kerja
            print(f"  • Rata-rata/hari: {rata_aktivitas:.1f} aktivitas, {rata_item:.1f} item")
    
    Utils.pause_and_back()

def tampilkan_detail_histori(aktivitas):
    """Menampilkan detail lengkap sebuah histori"""
    Utils.print_header("📄 Detail Histori")
    
    print(f"\n📋 INFORMASI AKTIVITAS")
    print("═" * 50)
    print(f"Nama Makanan     : {aktivitas['nama']}")
    print(f"Jumlah           : {aktivitas['jumlah']}")
    print(f"Kategori         : {aktivitas['jenis_makanan']}")
    print(f"Status           : {get_status_icon(aktivitas['status'])} {aktivitas['status']}")
    
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
    
    Utils.pause_and_back()

def calculate_time_ago(timestamp):
    """Menghitung berapa lama yang lalu aktivitas terjadi"""
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
    """Mengembalikan pesan berdasarkan status"""
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