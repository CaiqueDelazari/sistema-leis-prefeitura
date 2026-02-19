"""
Atualiza a senha do usuário 'admin' para o hash correto.
Depois use: Login = admin, Senha = Admin@123
"""
from app.config.database import get_connection
from werkzeug.security import generate_password_hash

USUARIO = "admin"
SENHA_NOVA = "Admin@123"

def main():
    password_hash = generate_password_hash(SENHA_NOVA)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET password_hash = ? WHERE LOWER(username) = LOWER(?)",
        (password_hash, USUARIO),
    )
    conn.commit()
    if cursor.rowcount:
        print("Senha do admin atualizada com sucesso!")
        print(f"  Login: {USUARIO}")
        print(f"  Senha: {SENHA_NOVA}")
    else:
        print("Usuário 'admin' não encontrado. Rode: python criar_admin.py")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
