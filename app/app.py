from flask import Flask, redirect, url_for, session, render_template, request, flash
import os
from dotenv import load_dotenv
from app.routes.lei_routes import lei_bp
from app.routes.auth_routes import auth_bp
from app.services.auth_service import autenticar_usuario

def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Chave secreta para sessões (login)
    app.secret_key = os.getenv("SECRET_KEY", "chave-insegura-altere-no-.env")

    # Primeira tela: sempre a de login na raiz "/" (login obrigatório para o resto)
    @app.route("/", methods=["GET", "POST"])
    def index():
        if session.get("usuario_id"):
            return redirect(url_for("lei.inicio"))
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            senha = request.form.get("password") or ""
            usuario = autenticar_usuario(username, senha)
            if usuario:
                session["usuario_id"] = usuario["id"]
                session["usuario_nome"] = usuario["username"]
                session["is_admin"] = bool(usuario.get("is_admin"))
                flash("Login realizado com sucesso.", "sucesso")
                return redirect(url_for("lei.inicio"))
            flash("Usuário ou senha inválidos.", "erro")
        return render_template("login.html")

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lei_bp)

    return app
