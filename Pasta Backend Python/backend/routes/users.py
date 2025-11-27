from flask import Blueprint, request, jsonify
from models import Usuario, Atendimento, db
from utils import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("users", __name__)

@bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json() or {}
    if not all(k in data for k in ("nome","email","senha","tipo")):
        return jsonify({"msg":"Campos obrigatórios: nome, email, senha, tipo"}), 400
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"msg":"Já existe usuário com esse email"}), 400
    u = Usuario(nome=data["nome"], email=data["email"], tipo=data["tipo"])
    u.set_senha(data["senha"])
    db.session.add(u)
    db.session.commit()
    return jsonify({"msg":"Usuário criado","id": u.id}), 201

@bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    requester = get_jwt_identity()
    req_user = Usuario.query.get(requester)
    if req_user.id != user_id and req_user.tipo != "admin":
        return jsonify({"msg":"Somente admin pode recuperar outro usuário"}), 403
    u = Usuario.query.get_or_404(user_id)
    return jsonify({"id":u.id,"nome":u.nome,"email":u.email,"tipo":u.tipo})

@bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    requester = get_jwt_identity()
    if requester != user_id:
        return jsonify({"msg":"Só é permitido atualizar seu próprio usuário"}), 403
    data = request.get_json() or {}
    u = Usuario.query.get_or_404(user_id)
    if "email" in data and data["email"] != u.email:
        if Usuario.query.filter_by(email=data["email"]).first():
            return jsonify({"msg":"Email já em uso"}), 400
        u.email = data["email"]
    if "nome" in data:
        u.nome = data["nome"]
    if "senha" in data:
        u.set_senha(data["senha"])
    db.session.commit()
    return jsonify({"msg":"Atualizado"}), 200

@bp.route("/<int:user_id>/reset-senha", methods=["POST"])
@jwt_required()
@admin_required
def reset_senha(user_id):
    u = Usuario.query.get_or_404(user_id)
    default = "senha123"
    u.set_senha(default)
    db.session.commit()
    return jsonify({"msg":"Senha resetada para padrão"}), 200

@bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):
    u = Usuario.query.get_or_404(user_id)
    if Atendimento.query.filter_by(id_usuario=user_id).first():
        return jsonify({"msg":"Não é possível remover usuário com atendimentos vinculados"}), 400
    db.session.delete(u)
    db.session.commit()
    return jsonify({"msg":"Usuário removido"}), 200