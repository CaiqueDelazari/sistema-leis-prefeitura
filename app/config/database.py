import os
import sqlite3

# SQLite: arquivo na pasta do projeto (onde fica run.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.normpath(os.path.join(BASE_DIR, "prefeitura.db"))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _criar_tabelas(conn)
    return conn


def _criar_tabelas(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS leis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_lei INTEGER UNIQUE NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data_lei DATE NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS atos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            secao TEXT NOT NULL,
            subsecao TEXT NOT NULL,
            nome_lei TEXT NOT NULL,
            descricao_previa TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
