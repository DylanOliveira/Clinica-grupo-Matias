
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Paciente, Atendimento, Responsavel
from datetime import datetime

bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")


def parse_date(value):
    if not value:
        return None
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except Exception:
            return None
    return value

@bp.route('/', methods=['POST'])
@jwt_required()
def create_paciente():
    data = request.get_json() or {}
    required = ['cpf','nome','telefone','email','estado','cidade','bairro','cep','rua']
    if not all(k in data and data.get(k) for k in required):
        return jsonify({"msg":"Campos obrigatórios faltando"}), 400

    # verificação de duplicidade
    if Paciente.query.filter_by(cpf=data['cpf']).first():
        return jsonify({"msg":"CPF já cadastrado"}), 400
    if Paciente.query.filter_by(email=data['email']).first():
        return jsonify({"msg":"Email já cadastrado"}), 400

    # tratamento de responsavel
    responsavel_obj = None
    if data.get('responsavel'):
        r = data['responsavel']
        
        if not all(k in r and r.get(k) for k in ('cpf','nome','data_nasc')):
            return jsonify({"msg":"Responsável precisa de cpf, nome e data_nasc"}), 400
        
        responsavel_obj = Responsavel.query.filter_by(cpf=r['cpf']).first()
        if not responsavel_obj:
            responsavel_obj = Responsavel(
                cpf=r['cpf'],
                nome=r['nome'],
                data_nasc=parse_date(r['data_nasc']),
                email=r.get('email'),
                telefone=r.get('telefone')
            )
            db.session.add(responsavel_obj)
            db.session.flush()

    pac = Paciente(
        cpf=data['cpf'],
        nome=data['nome'],
        telefone=data['telefone'],
        email=data['email'],
        data_nasc=parse_date(data.get('data_nasc')),
        estado=data['estado'],
        cidade=data['cidade'],
        bairro=data['bairro'],
        cep=data['cep'],
        rua=data['rua'],
        numero=data.get('numero'),
        responsavel=responsavel_obj
    )

    # Verificação de menor, exigir responsável
    if pac.is_menor():
        if not pac.responsavel:
            return jsonify({"msg":"Paciente menor requer responsável"}), 400
        
        if not pac.responsavel.data_nasc:
            return jsonify({"msg":"Data de nascimento do responsável é obrigatória"}), 400
        hoje = datetime.today().date()
        idade_respon = hoje.year - pac.responsavel.data_nasc.year - (
            (hoje.month, hoje.day) < (pac.responsavel.data_nasc.month, pac.responsavel.data_nasc.day)
        )
        if idade_respon < 18:
            return jsonify({"msg":"Responsável deve ter pelo menos 18 anos"}), 400

    db.session.add(pac)
    db.session.commit()
    return jsonify({"msg":"Paciente criado com sucesso", "id": pac.id}), 201

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_paciente(id):
    pac = Paciente.query.get_or_404(id)
    return jsonify(pac.to_dict()), 200

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_paciente(id):
    pac = Paciente.query.get_or_404(id)
    data = request.get_json() or {}

    # Verificação de duplicidade CPF / email
    if 'cpf' in data and data['cpf'] != pac.cpf:
        if Paciente.query.filter_by(cpf=data['cpf']).first():
            return jsonify({"msg":"CPF já em uso"}), 400
        pac.cpf = data['cpf']
    if 'email' in data and data['email'] != pac.email:
        if Paciente.query.filter_by(email=data['email']).first():
            return jsonify({"msg":"Email já em uso"}), 400
        pac.email = data['email']

    
    for campo in ["nome","telefone","data_nasc","estado","cidade","bairro","cep","rua","numero"]:
        if campo in data:
            if campo == 'data_nasc':
                pac.data_nasc = parse_date(data[campo])
            else:
                setattr(pac, campo, data[campo])

    # atualizar/atribuir responsável
    if 'responsavel' in data:
        r = data['responsavel']
        if r is None:
            
            pac.responsavel = None
        else:
            
            if 'id' in r:
                resp = Responsavel.query.get(r['id'])
                if not resp:
                    return jsonify({"msg":"Responsável informado não existe"}), 400
                pac.responsavel = resp
            else:
                
                resp = None
                if r.get('cpf'):
                    resp = Responsavel.query.filter_by(cpf=r['cpf']).first()
                if not resp:
                    if not all(k in r and r.get(k) for k in ('cpf','nome','data_nasc')):
                        return jsonify({"msg":"Para criar responsável são necessários cpf,nome,data_nasc"}), 400
                    resp = Responsavel(
                        cpf=r['cpf'],
                        nome=r['nome'],
                        data_nasc=parse_date(r['data_nasc']),
                        email=r.get('email'),
                        telefone=r.get('telefone')
                    )
                    db.session.add(resp)
                    db.session.flush()
                pac.responsavel = resp

    # Se for menor verificação que há responsável
    if pac.is_menor():
        if not pac.responsavel:
            return jsonify({"msg":"Responsável obrigatório para menores"}), 400
        hoje = datetime.today().date()
        idade_respon = hoje.year - pac.responsavel.data_nasc.year - (
            (hoje.month, hoje.day) < (pac.responsavel.data_nasc.month, pac.responsavel.data_nasc.day)
        )
        if idade_respon < 18:
            return jsonify({"msg":"Responsável deve ter pelo menos 18 anos"}), 400

    db.session.commit()
    return jsonify({"msg":"Paciente atualizado com sucesso"}), 200

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_paciente(id):
    pac = Paciente.query.get_or_404(id)
    # impedir exclusão se tiver atendimento
    if Atendimento.query.filter_by(id_paciente=id).first():
        return jsonify({"msg":"Não é possível excluir paciente com atendimentos registrados"}), 400
    db.session.delete(pac)
    db.session.commit()
    return jsonify({"msg":"Paciente removido com sucesso"}), 200

# Rota específica para remover responsável
@bp.route('/<int:id>/responsavel', methods=['DELETE'])
@jwt_required()
def delete_responsavel(id):
    pac = Paciente.query.get_or_404(id)
    if not pac.responsavel:
        return jsonify({"msg":"Paciente não possui responsável"}), 404
    
    if pac.is_menor():
        return jsonify({"msg":"Não é permitido remover responsável enquanto paciente for menor"}), 400
    
    pac.responsavel = None
    db.session.commit()
    return jsonify({"msg":"Responsável desvinculado"}), 200

# Listagem paginada de pacientes 
@bp.route('/', methods=['GET'])
@jwt_required()
def list_pacientes():
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = Paciente.query

    
    if request.args.get('nome'):
        query = query.filter(Paciente.nome.ilike(f"%{request.args.get('nome')}%"))
    if request.args.get('cpf'):
        query = query.filter_by(cpf=request.args.get('cpf'))

    pag = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [p.to_dict() for p in pag.items]
    return jsonify({
        'total': pag.total,
        'page': pag.page,
        'per_page': pag.per_page,
        'items': items
    }), 200
