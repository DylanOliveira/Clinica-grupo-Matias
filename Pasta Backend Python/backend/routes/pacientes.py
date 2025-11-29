from flask import Blueprint, request, jsonify
from models import Paciente, Atendimento, db
from flask_jwt_extended import jwt_required
from datetime import datetime

bp = Blueprint("pacientes", __name__)

@bp.route("/", methods=["POST"])
@jwt_required()
def create_paciente():
    data = request.get_json() or {}
    required = ("cpf","nome","telefone","email","estado","cidade","bairro","cep","rua")
    if not all(k in data for k in required):
        return jsonify({"msg":"Campos obrigatórios faltando"}), 400
    if Paciente.query.filter_by(cpf=data["cpf"]).first():
        return jsonify({"msg":"CPF já cadastrado"}), 400
    if Paciente.query.filter_by(email=data["email"]).first():
        return jsonify({"msg":"Email já cadastrado"}), 400

    pac = Paciente(
        cpf = data["cpf"],
        nome = data["nome"],
        telefone = data["telefone"],
        email = data["email"],
        data_nasc = datetime.fromisoformat(data["data_nasc"]).date() if data.get("data_nasc") else None,
        estado = data["estado"],
        cidade = data["cidade"],
        bairro = data["bairro"],
        cep = data["cep"],
        rua = data["rua"],
        numero = data.get("numero"),
        cpf_respon = data.get("cpf_respon"),
        nome_respon = data.get("nome_respon"),
        data_nasc_respon = datetime.fromisoformat(data["data_nasc_respon"]).date() if data.get("data_nasc_respon") else None,
        email_respon = data.get("email_respon"),
        telefone_respon = data.get("telefone_respon")
    )

    # se paciente menor, requer dados do responsável
    if pac.is_menor():
        if not (pac.cpf_respon and pac.nome_respon and pac.telefone_respon):
            return jsonify({"msg":"Paciente menor requer dados do responsável (cpf_respon, nome_respon, telefone_respon)"}), 400

    db.session.add(pac)
    db.session.commit()
    return jsonify({"msg":"Paciente criado","id": pac.id}), 201

@bp.route("/<int:paciente_id>", methods=["GET"])
@jwt_required()
def get_paciente(paciente_id):
    p = Paciente.query.get_or_404(paciente_id)
    return jsonify({
        "id": p.id,
        "nome": p.nome,
        "cpf": p.cpf,
        "email": p.email,
        "telefone": p.telefone
    })

@bp.route("/<int:paciente_id>", methods=["PUT"])
@jwt_required()
def update_paciente(paciente_id):
    data = request.get_json() or {}
    p = Paciente.query.get_or_404(paciente_id)
    if "cpf" in data and data["cpf"] != p.cpf:
        if Paciente.query.filter_by(cpf=data["cpf"]).first():
            return jsonify({"msg":"CPF já cadastrado"}), 400 #Verificação de repetição de CPF
        p.cpf = data["cpf"]
    if "email" in data and data["email"] != p.email:
        if Paciente.query.filter_by(email=data["email"]).first():
            return jsonify({"msg":"Email já cadastrado"}), 400 #Verificação de repetição de email
        p.email = data["email"]
    for field in ("nome","telefone","estado","cidade","bairro","cep","rua","numero","cpf_respon","nome_respon","email_respon","telefone_respon"):
        if field in data:
            setattr(p, field, data[field])
    if "data_nasc" in data:
        p.data_nasc = datetime.fromisoformat(data["data_nasc"]).date()
    if "data_nasc_respon" in data:
        p.data_nasc_respon = datetime.fromisoformat(data["data_nasc_respon"]).date()
    db.session.commit()
    return jsonify({"msg":"Paciente atualizado"}), 200

@bp.route("/<int:paciente_id>", methods=["DELETE"])
@jwt_required()
def delete_paciente(paciente_id):
    p = Paciente.query.get_or_404(paciente_id)
    if Atendimento.query.filter_by(id_paciente=paciente_id).first():
        return jsonify({"msg":"Não é possível remover paciente com atendimentos vinculados"}), 400
    db.session.delete(p)
    db.session.commit()
    return jsonify({"msg":"Paciente removido"}), 200
