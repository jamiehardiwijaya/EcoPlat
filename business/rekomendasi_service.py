from databases.makanan_repository import MakananRepository
from databases.bahan_repository import BahanRepository
from databases.resep_repository import ResepRepository
from state import AppState

class RecommendationService:

    @staticmethod
    def rekomendasi_dari_makanan():
        user_id = AppState.get_user_id()
        makanan_user = MakananRepository.get_by_user(user_id)

        if not makanan_user:
            return []

        semua_bahan = BahanRepository.get_all()
        rekomendasi = []
        sudah_ada = set()

        for makanan in makanan_user:
            kata_makanan = makanan["nama_makanan"].lower().split()

            for bahan in semua_bahan:
                nama_bahan = bahan["nama"].lower()
                cocok = False

                for kata in kata_makanan:
                    if len(kata) < 4:
                        continue

                    if kata == nama_bahan:
                        cocok = True

                    elif nama_bahan.startswith(kata):
                        cocok = True

                    if cocok:
                        break

                if not cocok:
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