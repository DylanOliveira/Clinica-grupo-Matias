from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate, validates, ValidationError
from models import Usuario, Paciente, Procedimento, Atendimento




class UsuarioSchema(SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True

    id = auto_field()
    nome = auto_field(required=True, validate=validate.Length(min=3))
    email = auto_field(required=True)
    tipo = auto_field(required=True)



class PacienteSchema(SQLAlchemySchema):
    class Meta:
        model = Paciente
        load_instance = True

    id = auto_field()
    cpf = auto_field(required=True)
    nome = auto_field(required=True)
    telefone = auto_field(required=True)
    email = auto_field(required=True)
    data_nasc = auto_field()

    estado = auto_field(required=True)
    cidade = auto_field(required=True)
    bairro = auto_field(required=True)
    cep = auto_field(required=True)
    rua = auto_field(required=True)
    numero = auto_field()

    cpf_respon = auto_field()
    nome_respon = auto_field()
    data_nasc_respon = auto_field()
    email_respon = auto_field()
    telefone_respon = auto_field()



class ProcedimentoSchema(SQLAlchemySchema):
    class Meta:
        model = Procedimento
        load_instance = True

    id = auto_field()
    nome = auto_field(required=True)
    descricao = auto_field(required=True)
    valor_plano = auto_field(required=True)
    valor_particular = auto_field(required=True)



class AtendimentoSchema(SQLAlchemySchema):
    class Meta:
        model = Atendimento
        load_instance = True

    id = auto_field()
    id_paciente = auto_field(required=True)
    id_usuario = auto_field(required=True)
    data_hora = auto_field(required=True)
    tipo = auto_field(required=True)
    numero_carteira = auto_field()
    valor_total = auto_field()

