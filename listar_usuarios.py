"""
Lista os usuários que estão no banco SQLite local (prefeitura.db).
Se aparecer vazio, crie o usuário: python criar_admin.py ou python criar_usuario.py
"""
from app.config.database import get_connection, DB_PATH

print("Banco usado pelo app (SQLite):", DB_PATH)
print("-" * 50)
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, username, is_admin FROM usuarios")
rows = cursor.fetchall()
cursor.close()
conn.close()

if not rows:
    print("Nenhum usuário no banco. Rode: python criar_usuario.py")
else:
    for r in rows:
        print(f"  id={r[0]}  usuario={r[1]}  admin={bool(r[2])}")
