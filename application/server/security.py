from server.models import (
    DBSession,
    Group,
    User,
    UserInGroup,
    )
from server.views import log


def groupfinder(name: str, request):
    user = DBSession.query(User).filter_by(name=name).first()

    groups_names = DBSession.query(Group.name).filter(Group.id.in_(
        DBSession.query(UserInGroup.group_id).filter_by(
            user_id=user.id))).first()

    return list(groups_names)
