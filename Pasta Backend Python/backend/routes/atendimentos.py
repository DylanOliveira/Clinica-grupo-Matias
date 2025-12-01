
from flask import Blueprint, request, jsonify
from models import Atendimento, Paciente, Procedimento, AtendimentoProcedimento, db, Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint("atendimentos", __name__, url_prefix="/atendimentos")

@bp.route('/', methods=['POST'])
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

@bp.route('/<int:atendimento_id>', methods=['GET'])
@jwt_required()
def get_atendimento(atendimento_id):
    # BAREMA 38 - consulta por id
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

@bp.route('/<int:atendimento_id>', methods=['PUT'])
@jwt_required()
def update_atendimento(atendimento_id):
    # admin para fazer alteração
    data = request.get_json() or {}
    a = Atendimento.query.get_or_404(atendimento_id)
    requester = get_jwt_identity()
    requester_user = Usuario.query.get(requester)
    if requester_user.tipo != "admin" and a.id_usuario != requester:
        return jsonify({"msg":"Somente admin ou criador podem alterar este atendimento"}), 403

    # permitir atualizações de procedimentos
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
        tipo = data.get("tipo", a.tipo)
        for proc in procedimentos_objects:
            total += float(proc.valor_plano) if tipo == "plano" else float(proc.valor_particular)
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

@bp.route('/<int:atendimento_id>', methods=['DELETE'])
@jwt_required()
def delete_atendimento(atendimento_id):
    #autorização de4 adm para deletar
    a = Atendimento.query.get_or_404(atendimento_id)
    requester = get_jwt_identity()
    requester_user = Usuario.query.get(requester)
    if requester_user.tipo != "admin" and a.id_usuario != requester:
        return jsonify({"msg":"Somente admin ou criador podem deletar este atendimento"}), 403
    AtendimentoProcedimento.query.filter_by(id_atendimento=atendimento_id).delete()
    db.session.delete(a)
    db.session.commit()
    return jsonify({"msg":"Atendimento removido"}), 200

@bp.route('/', methods=['GET'])
@jwt_required()
def list_atendimentos():
    #paginação de atendimentos e filtro entre datas
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = Atendimento.query
    if request.args.get('id_paciente'):
        query = query.filter_by(id_paciente=int(request.args.get('id_paciente')))
    if request.args.get('tipo'):
        query = query.filter_by(tipo=request.args.get('tipo'))
    if request.args.get('data_inicio'):
        try:
            dt_inicio = datetime.fromisoformat(request.args.get('data_inicio'))
            query = query.filter(Atendimento.data_hora >= dt_inicio)
        except Exception:
            return jsonify({"msg":"Formato de data_inicio inválido (ISO)"}), 400
    if request.args.get('data_fim'):
        try:
            dt_fim = datetime.fromisoformat(request.args.get('data_fim'))
            query = query.filter(Atendimento.data_hora <= dt_fim)
        except Exception:
            return jsonify({"msg":"Formato de data_fim inválido (ISO)"}), 400
    pag = query.paginate(page=page, per_page=per_page, error_out=False)
    items = []
    for a in pag.items:
        items.append({
            'id': a.id,
            'id_paciente': a.id_paciente,
            'id_usuario': a.id_usuario,
            'data_hora': a.data_hora.isoformat(),
            'tipo': a.tipo,
            'valor_total': str(a.valor_total)
        })
    return jsonify({'total': pag.total,'page': pag.page,'per_page': pag.per_page,'items': items}), 200
