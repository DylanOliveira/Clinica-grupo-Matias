

from app import create_app
from models import db, Usuario

def main():
    app = create_app()
    with app.app_context():

        # verificação de admin
        existente = Usuario.query.filter_by(email="admin@clinica.com").first()
        if existente:
            print("⚠ Já existe um admin cadastrado com esse e-mail.")
            return

        # Criação do usuário admin
        admin = Usuario(
            nome="Administrador",
            email="admin@clinica.com",
            tipo="admin"
        )
        admin.set_senha("admin123")  # senha do adm

        db.session.add(admin)
        db.session.commit()

        print("✔ Usuário ADMIN criado com sucesso!")
        print("   Email: admin@clinica.com")
        print("   Senha: admin123")

if __name__ == "__main__":
    main()
