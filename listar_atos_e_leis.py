"""
Lista atos e leis do banco SQLite local (prefeitura.db).
Rode na pasta do projeto: python listar_atos_e_leis.py
"""
from app.config.database import get_connection, DB_PATH

print("Banco (SQLite):", DB_PATH)
print()

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, secao, subsecao, nome_lei, descricao_previa FROM atos ORDER BY id DESC LIMIT 20")
atos = cursor.fetchall()
print("--- ATOS (últimos 20) ---")
if not atos:
    print("  (nenhum ato)")
else:
    for r in atos:
        print(f"  id={r[0]} | {r[1]} > {r[2]} | {r[3]}")

cursor.execute("SELECT id, numero_lei, titulo, data_lei FROM leis ORDER BY id DESC LIMIT 20")
leis = cursor.fetchall()
print()
print("--- LEIS (últimos 20) ---")
if not leis:
    print("  (nenhuma lei)")
else:
    for r in leis:
        print(f"  id={r[0]} | nº {r[1]} | {r[2]} | {r[3]}")

cursor.close()
conn.close()
