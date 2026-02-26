from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.lei_service import gerar_proximo_numero, salvar_lei, buscar_leis
from app.config.database import get_connection
from app.routes.auth_routes import login_obrigatorio

lei_bp = Blueprint("lei", __name__)


@lei_bp.route("/inicio")
@login_obrigatorio
def inicio():
    """Tela após o login: Adicionar Lei ou Procurar Lei."""
    return render_template("inicio.html")


@lei_bp.route("/adicionar", methods=["GET", "POST"])
@login_obrigatorio
def adicionar():
    """Tela única: Atos oficiais + Nova lei. POST salva os dois juntos (ato vinculado à lei)."""
    if request.method == "POST":
        secao = (request.form.get("secao") or "").strip()
        subsecao = (request.form.get("subsecao") or "").strip() or "Nenhuma"
        titulo = request.form.get("titulo", "").strip()
        descricao = (request.form.get("descricao") or "").strip()
        data_lei = request.form.get("data_lei", "").strip()

        if not secao:
            flash("Seção é obrigatória.", "erro")
            return redirect(url_for("lei.adicionar"))
        if not titulo or not data_lei:
            flash("Título e data da lei são obrigatórios.", "erro")
            return redirect(url_for("lei.adicionar"))

        numero = gerar_proximo_numero()
        cadastrado_por = session.get("usuario_nome") or ""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leis (numero_lei, titulo, descricao, data_lei, cadastrado_por) VALUES (?, ?, ?, ?, ?)",
                (numero, titulo, descricao, data_lei, cadastrado_por),
            )
            lei_id = cursor.lastrowid
            nome_lei = titulo or "Lei nº " + str(numero)
            cursor.execute(
                "INSERT INTO atos (lei_id, secao, subsecao, nome_lei, descricao_previa, cadastrado_por) VALUES (?, ?, ?, ?, ?, ?)",
                (lei_id, secao, subsecao, nome_lei, descricao, cadastrado_por),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            flash(f"Erro ao salvar: {e}", "erro")
            return redirect(url_for("lei.adicionar"))

        flash("Lei e ato oficial salvos com sucesso.", "sucesso")
        return redirect(url_for("lei.adicionar"))

    numero = gerar_proximo_numero()
    return render_template("adicionar.html", numero_lei=numero)


@lei_bp.route("/procurar-lei", methods=["GET", "POST"])
@login_obrigatorio
def procurar_lei():
    """Pesquisa de leis por data, login, título ou nome da lei."""
    leis = []
    if request.method == "POST":
        data_lei = (request.form.get("data_lei") or "").strip()
        cadastrado_por = (request.form.get("cadastrado_por") or "").strip()
        titulo = (request.form.get("titulo") or "").strip()
        nome_lei = (request.form.get("nome_lei") or "").strip()
        leis = buscar_leis(
            data_lei=data_lei or None,
            cadastrado_por=cadastrado_por or None,
            titulo=titulo or None,
            nome_lei=nome_lei or None,
        )
    return render_template("procurar_lei.html", leis=leis)


@lei_bp.route("/atos", methods=["GET", "POST"])
@login_obrigatorio
def atos():
    return redirect(url_for("lei.adicionar"))


@lei_bp.route("/nova-lei", methods=["GET", "POST"])
@login_obrigatorio
def nova_lei():
    return redirect(url_for("lei.adicionar"))

@lei_bp.route("/sucesso")
@login_obrigatorio
def sucesso():
    numero = request.args.get("numero")
    return render_template("sucesso.html", numero_lei=numero)
