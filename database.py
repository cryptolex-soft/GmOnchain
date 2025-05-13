import sqlite3
import os
from datetime import datetime
from config import NETWORKS

DB_NAME = "gm.db"


def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Формируем SQL с колонками по всем сетям
        columns = ",\n".join(
            [f"last_gm_{net} TEXT" for net in NETWORKS.keys()]
        )

        c.execute(f'''
            CREATE TABLE wallets (
                address TEXT PRIMARY KEY,
                private_key TEXT NOT NULL,
                last_gm_soneium TEXT,
                last_gm_unichain TEXT,
                last_gm_base TEXT,
                last_gm_ink TEXT,
                last_gm_mode TEXT,
                last_gm_lisk TEXT,
                last_gm_optimism TEXT
            )
        ''')
        conn.commit()
        conn.close()


def get_wallets():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    columns = ["address", "private_key"] + [f"last_gm_{net}" for net in NETWORKS]
    sql = f"SELECT {', '.join(columns)} FROM wallets"
    
    c.execute(sql)
    rows = c.fetchall()
    conn.close()

    wallets = [dict(zip(columns, row)) for row in rows]
    return wallets



def update_gm_timestamp(address, network):
    """Обновляет last_gm_<network> для указанного адреса"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    column = f"last_gm_{network}"
    now = datetime.utcnow().isoformat()
    c.execute(f"UPDATE wallets SET {column} = ? WHERE address = ?", (now, address))
    conn.commit()
    conn.close()



def insert_wallet(address, private_key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Подготовка всех столбцов с last_gm_<net> как NULL по умолчанию
    columns = ", ".join(["address", "private_key"] + [f"last_gm_{net}" for net in NETWORKS])
    placeholders = ", ".join(["?"] * (2 + len(NETWORKS)))
    values = [address, private_key] + [None for _ in NETWORKS]

    sql = f"INSERT OR IGNORE INTO wallets ({columns}) VALUES ({placeholders})"
    c.execute(sql, values)
    conn.commit()
    conn.close()
