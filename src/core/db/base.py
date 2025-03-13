from sqlalchemy import MetaData, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from datetime import datetime
from typing import TYPE_CHECKING


convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': "uq_%(table_name)s_%(column_0_name)s",
    'ck': "ck_%(table_name)s_%(column_0_name)s",
    'fk': "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    'pk': "pk_%(table_name)s"
}


Base = declarative_base()
Base.metadata = MetaData(naming_convention=convention)

class BaseModel(Base):
    """ The base class of all application models """

    __abstract__ = True

    if TYPE_CHECKING:   # pragma: no cover
        id: int
    else:
        id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'

__all__ = (
    'Base',
    'BaseModel',
)