from flask import Blueprint, request, jsonify
from models import Atendimento, Paciente, Procedimento, AtendimentoProcedimento, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from utils import admin_required

bp = Blueprint("atendimentos", __name__)

@bp.route("/", methods=["POST"])
@jwt_required()
def create_atendimento():
    data = request.get_json() or {}
    if not all(k in data for k in ("id_paciente","data_hora","tipo","procedimentos")):
        return jsonify({"msg":"Campos obrigatórios faltando (id_paciente, data_hora, tipo, procedimentos)"}), 400
    if not isinstance(data["procedimentos"], list) or len(data["procedimentos"]) == 0:
        return jsonify({"msg":"Atendimento precisa ter ao menos um procedimento"}), 400
    paciente = Paciente.query.get(data["id_paciente"])
    if not paciente:
        return jsonify({"msg":"Paciente não encontrado"}), 404
    if data["tipo"] == "plano" and not data.get("numero_carteira"):
        return jsonify({"msg":"Número da carteira obrigatório para tipo 'plano'"}), 400

    total = 0
    procedimentos_objects = []
    for pid in data["procedimentos"]:
        proc = Procedimento.query.get(pid)
        if not proc:
            return jsonify({"msg":f"Procedimento {pid} não encontrado"}), 404
        if data["tipo"] == "plano":
            total += float(proc.valor_plano)
        else:
            total += float(proc.valor_particular)
        procedimentos_objects.append(proc)

    atendimento = Atendimento(
        id_paciente = paciente.id,
        id_usuario = get_jwt_identity(),
        data_hora = datetime.fromisoformat(data["data_hora"]),
        tipo = data["tipo"],
        numero_carteira = data.get("numero_carteira"),
        valor_total = total
    )
    db.session.add(atendimento)
    db.session.commit()

    for proc in procedimentos_objects:
        ap = AtendimentoProcedimento(id_atendimento=atendimento.id, id_procedimento=proc.id)
        db.session.add(ap)
    db.session.commit()
    return jsonify({"msg":"Atendimento criado","id": atendimento.id}), 201

@bp.route("/<int:atendimento_id>", methods=["GET"])
@jwt_required()
def get_atendimento(atendimento_id):
    a = Atendimento.query.get_or_404(atendimento_id)
    procedimentos = [{"id":p.id,"nome":p.nome} for p in a.procedimentos]
    return jsonify({
        "id": a.id,
        "id_paciente": a.id_paciente,
        "id_usuario": a.id_usuario,
        "data_hora": a.data_hora.isoformat(),
        "tipo": a.tipo,
        "numero_carteira": a.numero_carteira,
        "valor_total": str(a.valor_total),
        "procedimentos": procedimentos
    })

@bp.route("/<int:atendimento_id>", methods=["PUT"])
@jwt_required()
def update_atendimento(atendimento_id):
    data = request.get_json() or {}
    a = Atendimento.query.get_or_404(atendimento_id)
    requester = get_jwt_identity()
    # somente admin ou criador pode alterar
    from models import Usuario
    requester_user = Usuario.query.get(requester)
    if requester_user.tipo != "admin" and a.id_usuario != requester:
        return jsonify({"msg":"Somente admin ou criador podem alterar este atendimento"}), 403

    # permitir atualizar procedimentos, data_hora, tipo (recalcular valor)
    if "procedimentos" in data:
        if not isinstance(data["procedimentos"], list) or len(data["procedimentos"]) == 0:
            return jsonify({"msg":"Procedimentos inválidos"}), 400
        total = 0
        procedimentos_objects = []
        for pid in data["procedimentos"]:
            proc = Procedimento.query.get(pid)
            if not proc:
                return jsonify({"msg":f"Procedimento {pid} não encontrado"}), 404
            procedimentos_objects.append(proc)
            # temporário: use tipo do payload se houver, senão tipo atual
        tipo = data.get("tipo", a.tipo)
        for proc in procedimentos_objects:
            total += float(proc.valor_plano) if tipo == "plano" else float(proc.valor_particular)
        # remover relações antigas
        AtendimentoProcedimento.query.filter_by(id_atendimento=a.id).delete()
        for proc in procedimentos_objects:
            ap = AtendimentoProcedimento(id_atendimento=a.id, id_procedimento=proc.id)
            db.session.add(ap)
        a.valor_total = total

    if "data_hora" in data:
        a.data_hora = datetime.fromisoformat(data["data_hora"])
    if "tipo" in data:
        a.tipo = data["tipo"]
        if a.tipo == "plano" and not data.get("numero_carteira") and not a.numero_carteira:
            return jsonify({"msg":"Número da carteira obrigatório para tipo 'plano'"}), 400
        a.numero_carteira = data.get("numero_carteira", a.numero_carteira)

    db.session.commit()
    return jsonify({"msg":"Atendimento atualizado"}), 200

@bp.route("/<int:atendimento_id>", methods=["DELETE"])
@jwt_required()
def delete_atendimento(atendimento_id):
    a = Atendimento.query.get_or_404(atendimento_id)
    requester = get_jwt_identity()
    from models import Usuario
    requester_user = Usuario.query.get(requester)
    if requester_user.tipo != "admin" and a.id_usuario != requester:
        return jsonify({"msg":"Somente admin ou criador podem deletar este atendimento"}), 403
    # atendimento_procedimento tem ON DELETE CASCADE, mas vamos garantir remoção
    AtendimentoProcedimento.query.filter_by(id_atendimento=atendimento_id).delete()
    db.session.delete(a)
    db.session.commit()
    return jsonify({"msg":"Atendimento removido"}), 200