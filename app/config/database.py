import os
import sqlite3

# Pasta do projeto: o banco fica aqui, arquivo único (SQLite local)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.normpath(os.path.join(_PROJECT_ROOT, "prefeitura.db"))


def get_connection():
    """
    Conexão com o banco SQLite local (arquivo prefeitura.db na pasta do projeto).
    Tudo (usuários, atos, leis) é salvo nesse arquivo. Não precisa de pgAdmin nem PostgreSQL.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _criar_tabelas_se_nao_existirem(conn)
    return conn


def _criar_tabelas_se_nao_existirem(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS leis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_lei INTEGER UNIQUE NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data_lei DATE NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cadastrado_por TEXT
        );
        CREATE TABLE IF NOT EXISTS atos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lei_id INTEGER REFERENCES leis(id),
            secao TEXT NOT NULL,
            subsecao TEXT NOT NULL,
            nome_lei TEXT NOT NULL,
            descricao_previa TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cadastrado_por TEXT
        );
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # Migração: colunas adicionadas depois
    cur = conn.cursor()
    for tabela in ("leis", "atos"):
        try:
            cur.execute(f"ALTER TABLE {tabela} ADD COLUMN cadastrado_por TEXT")
        except sqlite3.OperationalError:
            pass
    try:
        cur.execute("ALTER TABLE atos ADD COLUMN lei_id INTEGER REFERENCES leis(id)")
    except sqlite3.OperationalError:
        pass
    conn.commit()
