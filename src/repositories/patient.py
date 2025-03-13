from models import Patient
from core.db.repository import SQLAlchemyRepository

class PatientRepository(SQLAlchemyRepository[Patient]):
    model = Patient

__all__ = (
    'PatientRepository',
)
