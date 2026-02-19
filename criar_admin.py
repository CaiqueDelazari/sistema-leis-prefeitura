"""
Cria o usuário admin no banco SQLite local para você conseguir logar.
Usuário: admin
Senha: Admin@123
"""
from app.config.database import get_connection
from werkzeug.security import generate_password_hash

USUARIO = "admin"
SENHA = "Admin@123"

def main():
    password_hash = generate_password_hash(SENHA)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, is_admin) VALUES (?, ?, ?)",
            (USUARIO, password_hash, 1),
        )
        conn.commit()
        print(f"Usuário criado com sucesso!")
        print(f"  Login: {USUARIO}")
        print(f"  Senha: {SENHA}")
        print("\nAcesse http://127.0.0.1:5000/login e faça login.")
    except Exception as e:
        if "UNIQUE" in str(e) or "unique" in str(e).lower():
            print(f"O usuário '{USUARIO}' já existe. Use esse login e senha, ou rode criar_usuario.py para outro usuário.")
        else:
            print("Erro:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
