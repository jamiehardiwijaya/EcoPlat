from business.rekomendasi_service import RecommendationService
from utils.helper import Utils

def tampilkan_rekomendasi():
    Utils.print_header("Rekomendasi Resep", clear=True)

    rekomendasi = RecommendationService.rekomendasi_dari_makanan()

    if not rekomendasi:
        print("Tidak ada rekomendasi saat ini.")
        Utils.pause_and_back()
        return

    print("\nRekomendasi resep untukmu:")
    for i, item in enumerate(rekomendasi, start=1):
        resep = item["resep"]
        makanan_asal = item["makanan_asal"]
        print(f"{i}. Dari {makanan_asal} → {resep['nama_resep']} - {resep['deskripsi']}")

    Utils.pause_and_back()