from flask import Blueprint, request, jsonify
from models import Usuario, db
from flask_jwt_extended import create_access_token

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    if not data.get("email") or not data.get("senha"):
        return jsonify({"msg":"email e senha obrigatórios"}), 400

    user = Usuario.query.filter_by(email=data["email"]).first()
    if not user or not user.check_senha(data["senha"]):
        return jsonify({"msg":"credenciais inválidas"}), 401

    access_token = create_access_token(identity=user.id)
    user_data = {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "tipo": user.tipo
    }
    return jsonify({"access_token": access_token, "user": user_data}), 200