from flask import Blueprint, request, jsonify
# from flask_jwt_extended import create_access_token
# from werkzeug.security import check_password_hash
from core.middleware.auth_middleware import token_required
from core.settings.app import app
from users.router import auth_bp
from patients.router import patient_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(patient_bp, url_prefix='/api')

@app.route("/")
# @token_required
def home():
    return jsonify(message='Hello world !')
