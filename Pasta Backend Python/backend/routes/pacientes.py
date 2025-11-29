from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Paciente, Atendimento
from datetime import date

bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")


#Verificação de idade dos pacientes
def calcular_idade(data_nasc):
    hoje = date.today()
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))



@bp.route("/", methods=["POST"])
@jwt_required()
def create_paciente():
    data = request.get_json()

    # Verificar duplicidade de CPF
    if Paciente.query.filter_by(cpf=data.get("cpf")).first():
        return jsonify({"msg": "CPF já cadastrado"}), 400

    # Verificar duplicidade de e-mail
    if Paciente.query.filter_by(email=data.get("email")).first():
        return jsonify({"msg": "Email já cadastrado"}), 400

    try:
        pac = Paciente(
            cpf=data.get("cpf"),
            nome=data.get("nome"),
            telefone=data.get("telefone"),
            email=data.get("email"),
            data_nasc=data.get("data_nasc"),

            estado=data.get("estado"),
            cidade=data.get("cidade"),
            bairro=data.get("bairro"),
            cep=data.get("cep"),
            rua=data.get("rua"),

            cpf_respon=data.get("cpf_respon"),
            nome_respon=data.get("nome_respon"),
            data_nasc_respon=data.get("data_nasc_respon"),
            email_respon=data.get("email_respon"),
            telefone_respon=data.get("telefone_respon"),
        )
    except Exception as e:
        return jsonify({"msg": f"Erro nos dados enviados: {e}"}), 400


    if pac.is_menor():

        
        if not (pac.cpf_respon and pac.nome_respon and pac.telefone_respon and pac.data_nasc_respon):
            return jsonify({
                "msg": "Paciente menor requer responsável com CPF, nome, telefone e data de nascimento."
            }), 400

        #Verificação de maior de idade
        idade_respon = calcular_idade(pac.data_nasc_respon)
        if idade_respon < 18:
            return jsonify({"msg": "O responsável deve ter pelo menos 18 anos."}), 400


    db.session.add(pac)
    db.session.commit()

    return jsonify({"msg": "Paciente criado com sucesso", "id": pac.id}), 201



@bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_paciente(id):
    pac = Paciente.query.get(id)
    if not pac:
        return jsonify({"msg": "Paciente não encontrado"}), 404

    return jsonify(pac.to_dict()), 200



@bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_paciente(id):
    pac = Paciente.query.get(id)
    if not pac:
        return jsonify({"msg": "Paciente não encontrado"}), 404

    data = request.get_json()

    # Atualiza somente campos enviados
    for campo in [
        "cpf", "nome", "telefone", "email", "data_nasc",
        "estado", "cidade", "bairro", "cep", "rua",
        "cpf_respon", "nome_respon", "data_nasc_respon",
        "email_respon", "telefone_respon"
    ]:
        if campo in data:
            setattr(pac, campo, data[campo])


    if pac.is_menor():

        
        if not (pac.cpf_respon and pac.nome_respon and pac.telefone_respon and pac.data_nasc_respon):
            return jsonify({
                "msg": "Responsável obrigatório para menores — CPF, nome, telefone e data de nascimento são necessários."
            }), 400

        # verificação de idade minima
        idade_respon = calcular_idade(pac.data_nasc_respon)
        if idade_respon < 18:
            return jsonify({"msg": "O responsável deve ter pelo menos 18 anos."}), 400

    db.session.commit()
    return jsonify({"msg": "Paciente atualizado com sucesso"}), 200



@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_paciente(id):
    pac = Paciente.query.get(id)
    if not pac:
        return jsonify({"msg": "Paciente não encontrado"}), 404

    # Impedir exclusão se tiver atendimento
    if Atendimento.query.filter_by(id_paciente=id).first():
        return jsonify({"msg": "Não é possível excluir paciente com atendimentos registrados"}), 400

    db.session.delete(pac)
    db.session.commit()

    return jsonify({"msg": "Paciente removido com sucesso"}), 200
