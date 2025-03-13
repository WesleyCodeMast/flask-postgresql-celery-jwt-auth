from marshmallow import Schema, fields
from core.settings.app import db

class BaseModel(db.Model):
    __abstract__ = True

    id=db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def serialize(self):
        """Method to serialize the model instance."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class User(BaseModel):
    __tablename__ = 'tb_user'
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    role = db.Column(db.Integer(), default=4)

class Patient(BaseModel):
    __tablename__ = 'tb_patients'
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(250))
    phone = db.Column(db.String(15))
