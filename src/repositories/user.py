from models import User
from core.db.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository[User]):
    model = User

__all__ = (
    'UserRepository',
)
