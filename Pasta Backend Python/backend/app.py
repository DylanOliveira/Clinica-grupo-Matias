from flask import Flask, jsonify
from config import Config
from models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    
    from routes.auth import bp as auth_bp
    from routes.users import bp as users_bp
    from routes.pacientes import bp as pacientes_bp
    from routes.procedimentos import bp as procedimentos_bp
    from routes.atendimentos import bp as atendimentos_bp

    
    #Importações de blueprints para organização
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(pacientes_bp, url_prefix="/pacientes")
    app.register_blueprint(procedimentos_bp, url_prefix="/procedimentos")
    app.register_blueprint(atendimentos_bp, url_prefix="/atendimentos")

    @app.route("/")
    def index():
        return jsonify({"ok": True, "msg": "API Clinica - em execução"})

    return app
