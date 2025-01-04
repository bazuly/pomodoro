from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr


# simple case Base class
# class Base(DeclarativeBase):
#     pass

# but we use custom version

class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
