from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from models import Usuario


def admin_required(fn):
@wraps(fn)
def wrapper(*args, **kwargs):
identity = get_jwt_identity()
if not identity:
return jsonify({"msg":"Token inválido"}), 401
user = Usuario.query.filter_by(id=identity).first()
if not user or user.tipo != 'admin':
return jsonify({"msg":"Ação permitida somente para admin"}), 403
return fn(*args, **kwargs)
return wrapper
