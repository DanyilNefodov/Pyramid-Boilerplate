from pyramid.httpexceptions import HTTPInternalServerError, HTTPNotFound
from pyramid.session import JSONSerializer
from pyramid.session import PickleSerializer

from server.models import (
    DBSession,
    User,
    )


class JSONSerializerWithPickleFallback(object):
    def __init__(self):
        self.json = JSONSerializer()
        self.pickle = PickleSerializer()

    def dumps(self, value):
        return self.json.dumps(value)

    def loads(self, value):
        try:
            return self.json.loads(value)
        except ValueError:
            return self.pickle.loads(value)


def groupfinder(name: str, request):
    try:
        user = DBSession.query(User).filter(User.name == name).first()

        if user is None:
            raise HTTPNotFound

        return user.groups()

    except Exception:
        raise HTTPInternalServerError
