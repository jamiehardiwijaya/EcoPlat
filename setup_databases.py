import sqlite3

con = sqlite3.connect("EcoPlat.db")
c = con.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS sisa_makanan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    nama_makanan TEXT NOT NULL,
    jumlah INTEGER,
    kategori TEXT,
    tanggal_kadaluarsa TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS resep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    nama_resep TEXT NOT NULL,
    deskripsi TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS rekomendasi_resep (
    makanan_id INTEGER,
    resep_id INTEGER,
    PRIMARY KEY (makanan_id, resep_id),
    FOREIGN KEY (makanan_id) REFERENCES sisa_makanan (id),
    FOREIGN KEY (resep_id) REFERENCES resep (id)
);
""")

c.execute('''
CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        sisa_makanan_id INTEGER,
        tanggal_kadaluwarsa DATE,
        jenis_makanan TEXT,
        jumlah INTEGER,
        status TEXT,
        nama TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(id),
        FOREIGN KEY(sisa_makanan_id) REFERENCES sisa_makanan(id)
    )
''')

con.commit()
con.close()