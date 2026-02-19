from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.lei_service import gerar_proximo_numero, salvar_lei
from app.config.database import get_connection
from app.routes.auth_routes import login_obrigatorio

lei_bp = Blueprint("lei", __name__)


@lei_bp.route("/atos", methods=["GET", "POST"])
@login_obrigatorio
def atos():
    if request.method == "POST":
        secao = (request.form.get("secao") or "").strip()
        subsecao = (request.form.get("subsecao") or "").strip() or "Nenhuma"
        nome_lei = (request.form.get("nome_lei") or "").strip()
        descricao_previa = (request.form.get("descricao_previa") or "").strip()

        if not secao or not nome_lei:
            flash("Seção e nome/número da lei são obrigatórios.", "erro")
            return render_template("atos.html")

        try:
            conn = get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO atos (secao, subsecao, nome_lei, descricao_previa) VALUES (?, ?, ?, ?)",
                    (secao, subsecao, nome_lei, descricao_previa),
                )
                conn.commit()
            finally:
                conn.close()
        except Exception as e:
            flash(f"Erro ao salvar ato: {e}", "erro")
            return render_template("atos.html")

        flash("Ato salvo com sucesso.", "sucesso")
        return redirect(url_for("lei.atos"))

    return render_template("atos.html")


@lei_bp.route("/nova-lei", methods=["GET", "POST"])
@login_obrigatorio
def nova_lei():
    numero = gerar_proximo_numero()
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = (request.form.get("descricao") or "").strip()
        data_lei = request.form.get("data_lei", "").strip()

        if not titulo or not data_lei:
            flash("Título e data da lei são obrigatórios.", "erro")
            return render_template("nova_lei.html", numero_lei=numero)

        try:
            salvar_lei(numero, titulo, descricao, data_lei)
        except Exception as e:
            flash(f"Erro ao salvar lei: {e}", "erro")
            return render_template("nova_lei.html", numero_lei=numero)

        flash("Lei cadastrada com sucesso.", "sucesso")
        return redirect(url_for("lei.sucesso", numero=numero))
    return render_template("nova_lei.html", numero_lei=numero)

@lei_bp.route("/sucesso")
@login_obrigatorio
def sucesso():
    numero = request.args.get("numero")
    return render_template("sucesso.html", numero_lei=numero)
