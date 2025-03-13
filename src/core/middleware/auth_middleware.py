import traceback
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
# from models import User
from core.settings import get_application_settings
from repositories.user import UserRepository
settings = get_application_settings()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {
                "message": "Authentication Token is missing !",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        try:
            data = jwt.decode(token, str(settings.SECRET_KEY), algorithms=["HS256"])

            user_repository = UserRepository(sync=True)
            current_user = user_repository.find_one(email=data.get('email'))
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

        except Exception as e:
            traceback.print_exc()
            return {
                "message": "Server went wrong!",
                "data": None,
                "error": "Unauthorized"
            }, 500
        
        return f(current_user, *args, **kwargs)
    
    return decorated
