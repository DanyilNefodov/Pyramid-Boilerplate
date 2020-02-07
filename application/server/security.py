from server.models import (
    DBSession,
    Group,
    User,
    UserInGroup,
    )


def groupfinder(name: str, request):
    user = DBSession.query(User).filter(User.name == name).first()

    groups_names = DBSession.query(Group.name).filter(Group.id.in_(
        DBSession.query(UserInGroup.group_id).filter(
            User.user_id == user.id))).first()

    return list(groups_names)
