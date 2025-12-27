from databases.makanan_repository import MakananRepository
from databases.bahan_repository import BahanRepository
from databases.resep_repository import ResepRepository
from state import AppState

class RecommendationService:

    RULES = {
        "ayam": "Ayam",
        "telur": "Telur",
        "nasi": "Nasi",
        "ikan": "Ikan",
        "daging": "Daging"
    }

    @staticmethod
    def rekomendasi_dari_makanan():
        user_id = AppState.get_user_id()
        makanan_user = MakananRepository.get_by_user(user_id)

        if not makanan_user:
            return []

        rekomendasi = []
        sudah_ada = set()

        for makanan in makanan_user:
            nama_makanan = makanan["nama_makanan"].lower()

            for keyword, nama_bahan in RecommendationService.RULES.items():
                if keyword in nama_makanan:

                    bahan = BahanRepository.get_by_name(nama_bahan)
                    if not bahan:
                        continue

                    resep_list = ResepRepository.get_resep_by_bahan(bahan["id"])

                    for resep in resep_list:
                        if resep["id"] not in sudah_ada:
                            rekomendasi.append({
                                "makanan_asal": makanan["nama_makanan"],
                                "resep": resep
                            })
                            sudah_ada.add(resep["id"])

        return rekomendasi