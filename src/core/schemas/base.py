from core.settings.app import db

class BaseModel(db.Model):
    __abstract__ = True

    id=db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def serialize(self):
        """Method to serialize the model instance."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

__all__ = (
    'BaseModel',
)