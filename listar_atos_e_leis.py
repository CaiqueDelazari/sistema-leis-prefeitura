"""
Lista atos e leis do banco SQLite local (prefeitura.db).
Rode na pasta do projeto: python listar_atos_e_leis.py
"""
from app.config.database import get_connection, DB_PATH

print("Banco (SQLite):", DB_PATH)
print()

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT id, secao, subsecao, nome_lei, data_cadastro, cadastrado_por
    FROM atos ORDER BY id DESC LIMIT 20
""")
atos = cursor.fetchall()
print("--- ATOS (últimos 20) ---")
if not atos:
    print("  (nenhum ato)")
else:
    for r in atos:
        data_cad = r[4] or "-"
        usuario = r[5] or "-"
        print(f"  id={r[0]} | {r[1]} > {r[2]} | {r[3]} | em {data_cad} por {usuario}")

cursor.execute("""
    SELECT id, numero_lei, titulo, data_lei, data_cadastro, cadastrado_por
    FROM leis ORDER BY id DESC LIMIT 20
""")
leis = cursor.fetchall()
print()
print("--- LEIS (últimos 20) ---")
if not leis:
    print("  (nenhuma lei)")
else:
    for r in leis:
        data_cad = r[4] or "-"
        usuario = r[5] or "-"
        print(f"  id={r[0]} | nº {r[1]} | {r[2]} | {r[3]} | em {data_cad} por {usuario}")

cursor.close()
conn.close()
