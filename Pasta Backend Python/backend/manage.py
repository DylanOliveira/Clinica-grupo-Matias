from flask.cli import FlaskGroup
from app import create_app
from models import db

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    db.create_all()
    print("Banco criado com sucesso!")

@cli.command("drop_db")
def drop_db():
    db.drop_all()
    print("Banco removido com sucesso!")

if __name__ == "__main__":
    cli()