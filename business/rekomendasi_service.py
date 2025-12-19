from databases.bahan_repository import BahanRepository
from databases.resep_repository import ResepRepository
from databases.makanan_repository import MakananRepository
from state import AppState

class RecommendationService:

    @staticmethod
    def rekomendasi_dari_makanan():
        user_id = AppState.get_user_id()
        makanan_list = MakananRepository.get_by_user(user_id)

        rekomendasi = []
        sudah_ada = set()

        semua_bahan = BahanRepository.get_all() 
        
        for makanan in makanan_list:
            nama_makanan_user = makanan['nama_makanan'].lower()
            
            for bahan in semua_bahan:
                if bahan['nama'].lower() in nama_makanan_user:  
                    resep_list = ResepRepository.get_resep_by_bahan(bahan['id'])
                    for resep in resep_list:
                        if resep['id'] not in sudah_ada:
                            rekomendasi.append({
                                'resep': resep,
                                'makanan_asal': makanan['nama_makanan']
                            })
                            sudah_ada.add(resep['id'])
        
        return rekomendasi