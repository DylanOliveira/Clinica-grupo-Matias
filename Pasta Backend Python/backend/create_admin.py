
from app import create_app
from models import db, Usuario

app = create_app()
with app.app_context():
    u = Usuario(nome="Admin Teste", email="admin@exemplo.com", tipo="admin")
    u.set_senha("senha_segura_aqui") 
    db.session.add(u)
    db.session.commit()
    print("Admin criado com id:", u.id)
