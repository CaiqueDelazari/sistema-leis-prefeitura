from werkzeug.security import generate_password_hash

senha = "Admin@123"  # senha que você quer usar
hash_gerado = generate_password_hash(senha)
print("\n" + "="*80)
print("HASH GERADO (copie tudo abaixo):")
print("="*80)
print(hash_gerado)
print("="*80)
print("\nUsuário: admin")
print("Senha: Admin@123")
print("\nCole o hash acima no SQL do pgAdmin!")
