from pyramid.httpexceptions import HTTPInternalServerError, HTTPNotFound

from server.models import (
    DBSession,
    User,
    )


def groupfinder(name: str, request):
    try:
        user = DBSession.query(User).filter(User.name == name).first()

        if user is None:
            raise HTTPNotFound

        return user.groups()

    except Exception:
        raise HTTPInternalServerError
