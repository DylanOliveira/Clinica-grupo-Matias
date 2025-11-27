from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import ENUM, DECIMAL, TEXT

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha_hash = db.Column(db.String(200), nullable=False)
    tipo = db.Column(ENUM('admin','padrao', name='user_types'), nullable=False)

    atendimentos = db.relationship("Atendimento", backref="usuario", lazy=True)

    def set_senha(self, senha_plain):
        self.senha_hash = generate_password_hash(senha_plain)

    def check_senha(self, senha_plain):
        return check_password_hash(self.senha_hash, senha_plain)

class Paciente(db.Model):
    __tablename__ = "pacientes"
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(15), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    data_nasc = db.Column(db.Date)
    estado = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    # opcional: numero do endereço
    numero = db.Column(db.String(20), nullable=True)

    cpf_respon = db.Column(db.String(15))
    nome_respon = db.Column(db.String(100))
    data_nasc_respon = db.Column(db.Date)
    email_respon = db.Column(db.String(100))
    telefone_respon = db.Column(db.String(20))

    atendimentos = db.relationship("Atendimento", backref="paciente", lazy=True)

    def is_menor(self):
        if not self.data_nasc:
            return False
        hoje = date.today()
        idade = hoje.year - self.data_nasc.year - ((hoje.month, hoje.day) < (self.data_nasc.month, self.data_nasc.day))
        return idade < 18

class Procedimento(db.Model):
    __tablename__ = "procedimentos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(TEXT, nullable=False)
    valor_plano = db.Column(DECIMAL(10,2), nullable=False)
    valor_particular = db.Column(DECIMAL(10,2), nullable=False)

class AtendimentoProcedimento(db.Model):
    __tablename__ = "atendimento_procedimento"
    id_atendimento = db.Column(db.Integer, db.ForeignKey('atendimentos.id', ondelete="CASCADE"), primary_key=True)
    id_procedimento = db.Column(db.Integer, db.ForeignKey('procedimentos.id', ondelete="CASCADE"), primary_key=True)

class Atendimento(db.Model):
    __tablename__ = "atendimentos"
    id = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(ENUM('plano','particular', name='atendimento_type'), nullable=False)
    numero_carteira = db.Column(db.String(50), nullable=True)
    valor_total = db.Column(DECIMAL(10,2), nullable=False)

    procedimentos = db.relationship("Procedimento", secondary="atendimento_procedimento", lazy='subquery')