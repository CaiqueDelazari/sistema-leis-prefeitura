from app.config.database import get_connection

def gerar_proximo_numero():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(numero_lei) FROM leis")
    ultimo = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return 1 if ultimo is None else ultimo + 1

def salvar_lei(numero, titulo, descricao, data_lei, cadastrado_por=None):
    """Salva lei com data/hora do cadastro e login de quem cadastrou."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO leis (numero_lei, titulo, descricao, data_lei, cadastrado_por) VALUES (?, ?, ?, ?, ?)",
            (numero, titulo, descricao, data_lei, cadastrado_por or ""),
        )
        conn.commit()
    finally:
        conn.close()


def buscar_leis(data_lei=None, cadastrado_por=None, titulo=None, nome_lei=None):
    """
    Busca leis por filtros opcionais: data da lei, login de quem cadastrou, título, nome/número da lei.
    Retorna lista de dicts com id, numero_lei, titulo, descricao, data_lei, data_cadastro, cadastrado_por.
    """
    conn = get_connection()
    cursor = conn.cursor()
    params = []
    where = []
    if data_lei:
        where.append("data_lei = ?")
        params.append(data_lei)
    if cadastrado_por:
        where.append("cadastrado_por LIKE ?")
        params.append("%" + cadastrado_por.strip() + "%")
    if titulo:
        where.append("titulo LIKE ?")
        params.append("%" + titulo.strip() + "%")
    if nome_lei:
        where.append("(titulo LIKE ? OR CAST(numero_lei AS TEXT) LIKE ?)")
        params.append("%" + nome_lei.strip() + "%")
        params.append("%" + nome_lei.strip() + "%")
    sql = "SELECT id, numero_lei, titulo, descricao, data_lei, data_cadastro, cadastrado_por FROM leis"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {
            "id": r[0],
            "numero_lei": r[1],
            "titulo": r[2],
            "descricao": r[3] or "",
            "data_lei": r[4],
            "data_cadastro": r[5] or "",
            "cadastrado_por": r[6] or "",
        }
        for r in rows
    ]
