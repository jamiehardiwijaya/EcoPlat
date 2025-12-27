import pandas as pd
import os
from datetime import datetime
from state import AppState
from databases.resep_repository import ResepRepository
from databases.bahan_resep_repo import BahanResepRepository
from databases.bahan_repository import BahanRepository

class RecipeRecoveryService:
    CSV_PATH = "deleted_recipes.csv"

    @staticmethod
    def _ensure_csv():
        if not os.path.exists(RecipeRecoveryService.CSV_PATH):
            df = pd.DataFrame(columns=[
                "id", "user_id", "nama_resep", "deskripsi",
                "bahan", "deleted_at", "is_recovered"
            ])
            df.to_csv(RecipeRecoveryService.CSV_PATH, index=False)

    @staticmethod
    def record_deleted_recipe(resep):
        RecipeRecoveryService._ensure_csv()

        df = pd.read_csv(RecipeRecoveryService.CSV_PATH)

        df = pd.concat([df, pd.DataFrame([{
            "id": resep["id"],
            "user_id": resep["user_id"],
            "nama_resep": resep["nama_resep"],
            "deskripsi": resep["deskripsi"],
            "bahan": ", ".join(resep["bahan"]),
            "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_recovered": 0
        }])], ignore_index=True)

        df.to_csv(RecipeRecoveryService.CSV_PATH, index=False)

    @staticmethod
    def get_deleted_recipes(user_id=None):
        RecipeRecoveryService._ensure_csv()
        user_id = AppState.get_user_id()

        df = pd.read_csv(RecipeRecoveryService.CSV_PATH)
        df = df[(df["user_id"] == user_id) & (df["is_recovered"] == 0)]

        return df.to_dict("records")

    @staticmethod
    def recover_recipe(recipe_id):
        RecipeRecoveryService._ensure_csv()
        user_id = AppState.get_user_id()

        df = pd.read_csv(RecipeRecoveryService.CSV_PATH)
        row = df[(df["id"] == recipe_id) & (df["is_recovered"] == 0)]

        if row.empty:
            return {"success": False, "message": "Resep tidak ditemukan"}

        data = row.iloc[0]

        resep_id = ResepRepository.tambah_resep(
            user_id,
            data["nama_resep"],
            data["deskripsi"]
        )

        bahan_list = data["bahan"].split(",")
        for nama in bahan_list:
            nama = nama.strip()
            bahan = BahanRepository.get_by_name_case_insensitive(nama.lower())
            if bahan:
                bahan_id = bahan["id"]
            else:
                bahan_id = BahanRepository.tambah_bahan(nama.capitalize())

            BahanResepRepository.tambah(resep_id, bahan_id)

        df.loc[df["id"] == recipe_id, "is_recovered"] = 1
        df.to_csv(RecipeRecoveryService.CSV_PATH, index=False)

        return {"success": True, "message": "Resep berhasil dipulihkan"}
    
    @staticmethod
    def permanently_delete_recipe(recipe_id):
        RecipeRecoveryService._ensure_csv()

        df = pd.read_csv(RecipeRecoveryService.CSV_PATH)

        before = len(df)
        df = df[df["id"] != recipe_id]
        after = len(df)

        df.to_csv(RecipeRecoveryService.CSV_PATH, index=False)

        if before == after:
            return {"success": False, "message": "Resep tidak ditemukan di arsip"}

        return {"success": True, "message": "Resep dihapus permanen"}
