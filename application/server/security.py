from server.models import (
    DBSession,
    Group,
    UserInGroup,
    )
from server.views import log


def groupfinder(user_id, request):
    groups_names = DBSession.query(Group.name).filter(Group.id.in_(DBSession.query(UserInGroup.group_id).filter_by(user_id=1))).all()
    return groups_names
