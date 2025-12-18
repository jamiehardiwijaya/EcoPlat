# import sqlite3
from databases.db import get_db_connection

def init_db():
    con = get_db_connection()
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
    CREATE TABLE IF NOT EXISTS bahan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama VARCHAR NOT NULL
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
    CREATE TABLE IF NOT EXISTS user_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            use  r_id INTEGER NOT NULL,
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
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS bahan_resep (
        resep_id INTEGER,
        bahan_id INTEGER,
        PRIMARY KEY (resep_id, bahan_id),
        FOREIGN KEY (resep_id) REFERENCES resep (id),
        FOREIGN KEY (bahan_id) REFERENCES bahan (id)
    );
    """)

    con.commit()
    con.close()
    
    print("Database berhasil diinisialisasi!")

if __name__ == "__main__":
    init_db()