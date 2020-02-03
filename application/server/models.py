from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    SmallInteger,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
    )

from sqlalchemy_imageattach.entity import Image, image_attachment

from zope.sqlalchemy import register

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    password = Column(Text)


class Banner(Base):
    __tablename__ = 'banner'
    
    STATUS_1, STATUS_2, STATUS_3 = range(3)
    STATUSES = (
        (0, "Status 1"),
        (1, "Status 2"),
        (2, "Status 3"),
    )

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    image_path = Column(Text, unique=True)
    url = Column(Text)
    status = Column(SmallInteger, default=STATUS_1)
    position = Column(Integer, unique=True)


class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Everyone, 'edit')]

    def __init__(self, request):
        pass