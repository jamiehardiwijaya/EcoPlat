from business.rekomendasi_service import RecommendationService

@staticmethod
def tampilkan_rekomendasi():
    rekomendasi = RecommendationService.rekomendasi_dari_makanan()
        
    if not rekomendasi:
        print("Tidak ada rekomendasi saat ini. Coba tambahkan lebih banyak makanan.")
        input("Tekan Enter untuk kembali...")
        return
        
    print("Rekomendasi resep untukmu:")
    for idx, item in enumerate(rekomendasi, start=1):
        resep = item['resep']
        makanan_asal = item['makanan_asal']
        print(f"{idx}. Dari {makanan_asal} → {resep['nama_resep']} - {resep['deskripsi']}")
        input("Tekan Enter untuk kembali...")