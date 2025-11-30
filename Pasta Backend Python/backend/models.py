from flask_sqlalchemy import SQLAlchemy
rua = db.Column(db.String(100), nullable=False)
numero = db.Column(db.String(20), nullable=True)


# agora referência para tabela Responsavel (opcional)
responsavel_id = db.Column(db.Integer, db.ForeignKey('responsaveis.id'), nullable=True)
responsavel = db.relationship('Responsavel', backref=db.backref('pacientes', lazy=True))


atendimentos = db.relationship("Atendimento", backref="paciente", lazy=True)


def calcular_idade(self):
if not self.data_nasc:
return None
hoje = date.today()
return hoje.year - self.data_nasc.year - ((hoje.month, hoje.day) < (self.data_nasc.month, self.data_nasc.day))


def is_menor(self):
idade = self.calcular_idade()
if idade is None:
return False
return idade < 18


def to_dict(self):
return {
"id": self.id,
"cpf": self.cpf,
"nome": self.nome,
"telefone": self.telefone,
"email": self.email,
"data_nasc": self.data_nasc.isoformat() if self.data_nasc else None,
"estado": self.estado,
"cidade": self.cidade,
"bairro": self.bairro,
"cep": self.cep,
"rua": self.rua,
"numero": self.numero,
"responsavel": {
"id": self.responsavel.id,
"cpf": self.responsavel.cpf,
"nome": self.responsavel.nome,
"data_nasc": self.responsavel.data_nasc.isoformat()
} if self.responsavel else None
}


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
