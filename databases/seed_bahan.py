from db import execute_query

def seed_bahan():
    bahan_list = [
        ("Nasi",),
        ("Ayam",),
        ("Telur",),
        ("Sayur",),
        ("Tahu",),
        ("Tempe",)
    ]

    for bahan in bahan_list:
        execute_query(
            "INSERT OR IGNORE INTO bahan (nama) VALUES (?)",
            bahan
        )

def seed_resep():
    resep_list = [
        ("Nasi Goreng", "Nasi goreng sederhana",),
        ("Ayam Goreng", "Ayam goreng crispy",),
        ("Telur Dadar", "Telur dadar praktis",),
    ]

    for resep in resep_list:
        execute_query(
            "INSERT OR IGNORE INTO resep (nama_resep, deskripsi) VALUES (?, ?)",
            resep
        )

def seed_bahan_resep():
    relasi = [
        (1, 1),  # Nasi → Nasi Goreng
        (2, 2),  # Ayam → Ayam Goreng
        (3, 3),  # Telur → Telur Dadar
        (1, 3),  # Nasi → Telur Dadar
    ]

    for r in relasi:
        execute_query(
            "INSERT OR IGNORE INTO bahan_resep (bahan_id, resep_id) VALUES (?, ?)",
            r
        )

def run_seed():
    seed_bahan()
    seed_resep()
    seed_bahan_resep()
    print("✓ Data dummy berhasil dimasukkan")

if __name__ == "__main__":
    run_seed()