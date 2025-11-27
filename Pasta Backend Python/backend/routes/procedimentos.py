from flask import Blueprint, request, jsonify
from models import Procedimento, AtendimentoProcedimento, db
from utils import admin_required
from flask_jwt_extended import jwt_required

bp = Blueprint("procedimentos", __name__)

@bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_procedimento():
    data = request.get_json() or {}
    required = ("nome","descricao","valor_plano","valor_particular")
    if not all(k in data for k in required):
        return jsonify({"msg":"Campos obrigatórios faltando"}), 400
    if Procedimento.query.filter_by(nome=data["nome"]).first():
        return jsonify({"msg":"Procedimento com esse nome já existe"}), 400
    p = Procedimento(
        nome=data["nome"],
        descricao=data["descricao"],
        valor_plano=data["valor_plano"],
        valor_particular=data["valor_particular"]
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"msg":"Procedimento criado","id": p.id}), 201

@bp.route("/<int:proc_id>", methods=["GET"])
@jwt_required()
def get_procedimento(proc_id):
    p = Procedimento.query.get_or_404(proc_id)
    return jsonify({"id":p.id,"nome":p.nome,"descricao":p.descricao,"valor_plano":str(p.valor_plano),"valor_particular":str(p.valor_particular)})

@bp.route("/<int:proc_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_procedimento(proc_id):
    data = request.get_json() or {}
    p = Procedimento.query.get_or_404(proc_id)
    if "nome" in data and data["nome"] != p.nome:
        if Procedimento.query.filter_by(nome=data["nome"]).first():
            return jsonify({"msg":"Nome já em uso"}), 400
        p.nome = data["nome"]
    for field in ("descricao","valor_plano","valor_particular"):
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify({"msg":"Procedimento atualizado"}), 200

@bp.route("/<int:proc_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_procedimento(proc_id):
    # verificar uso em atendimentos
    if AtendimentoProcedimento.query.filter_by(id_procedimento=proc_id).first():
        return jsonify({"msg":"Não é possível remover procedimento usado em atendimentos"}), 400
    p = Procedimento.query.get_or_404(proc_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"msg":"Procedimento removido"}), 200