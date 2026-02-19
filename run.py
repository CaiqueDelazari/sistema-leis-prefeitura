from app.app import create_app

app = create_app()

if __name__ == "__main__":
    from app.config.database import DB_PATH
    print("Banco (SQLite):", DB_PATH)
    print("Sem usuário? Rode: python criar_admin.py")
    app.run(debug=True)
