from server.core.db import Base


class BaseModel(Base):
    __abstract__ = True
    """ Base model class """

    @classmethod
    def pk_name(cls):
        """Pick"""
        return cls.__mapper__.primary_key[0].name

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
