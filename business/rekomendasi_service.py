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
            nama_makanan = makanan["nama_makanan"].lower()

            for bahan in semua_bahan:
                nama_bahan = bahan["nama"].lower()

                cocok = False

                # 1. substring langsung
                if nama_bahan in nama_makanan or nama_makanan in nama_bahan:
                    cocok = True

                # 2. prefix match (lasag ~ lasagna)
                if not cocok:
                    sama = 0
                    batas = min(len(nama_bahan), len(nama_makanan))
                    for i in range(batas):
                        if nama_bahan[i] == nama_makanan[i]:
                            sama += 1
                        else:
                            break
                    if sama >= 3:
                        cocok = True

                # 3. overlap huruf
                if not cocok:
                    huruf_sama = 0
                    for h in set(nama_bahan):
                        if h in nama_makanan:
                            huruf_sama += 1
                    if huruf_sama / max(len(set(nama_bahan)), 1) >= 0.6:
                        cocok = True

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
