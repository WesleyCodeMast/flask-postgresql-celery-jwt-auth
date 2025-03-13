from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from core.middleware.auth_middleware import token_required
from core.settings import get_application_settings
from core.validate import validate_email_and_password, validate_user
from repositories.user import UserRepository
from models import User
import traceback
import jwt
from core.settings.app import app
import datetime

settings = get_application_settings()

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return {
            "message": "Please provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    is_validated = validate_email_and_password(data.get('email'), data.get('password'))
    
    if is_validated is not True:
        return dict(message="Invalid data", data=None, error=is_validated), 400
    email = data.get('email')
    password = data.get('password')

    user_repository = UserRepository(sync=True)

    user = user_repository.find_one(email=email)

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if user:
        try:
            token = jwt.encode(
                {
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                },
                str(settings.SECRET_KEY),
                algorithm='HS256'
            )
            return {
                "message": "Successfully fetched auth token",
                "token": token
            }
        
        except Exception as e:
            traceback.print_exc()
            return {
                'error': 'Something went wrong.',
                'message': str(e)
            }, 500

    return {
        'error': 'Unauthorized',
        'data': None,
        'message': "Error fetching auth token!, invalid email or password",
    }, 404
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        
        is_validated = validate_user(**user)

        if is_validated is not True:
            return dict(message="Invalid data", data=None, error=is_validated), 400
        
        user_repository = UserRepository(sync=True)

        is_exist_user = user_repository.find_one(email=user.get('email'))
        if is_exist_user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        
        new_user = user_repository.create(
            name=user.get('name'),
            email=user.get('email'),
            password=generate_password_hash(user.get('password')),
            role=4
        )
    
        return {
            "message": "Successfully created new user",
            "data": {
                'name': new_user.name,
                'email': new_user.email
            }
        }, 201
    
    except Exception as e:
        traceback.print_exc()
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@auth_bp.route("/current_user", methods=["GET"])
@token_required
def get_current_user(current_user):
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": current_user
    })
