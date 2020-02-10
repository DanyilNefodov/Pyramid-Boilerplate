import datetime
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging)

from server.models import (
    Banner,
    Base,
    DBSession,
    Group,
    User,
    UserInGroup)
from server.password_utils import hash_password


def usage(argv):
    cmd = os.path.basename(argv[0])
    print(f'usage: {cmd} <config_uri>\n + (example: "{cmd} development.ini")')
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        # Create default models

        group = Group(
            name="group:admin"
        )
        DBSession.add(group)

        user = User(
            name='Test',
            password=hash_password('1234')
        )
        DBSession.add(user)

        new_group_id = int(DBSession.query(
            Group).filter(Group.name == group.name).first().id)

        new_user_id = int(DBSession.query(User).filter(
            User.name == user.name).first().id)

        user_in_group = UserInGroup(
            user_id=new_user_id,
            group_id=new_group_id
        )
        DBSession.add(user_in_group)

        # for bid in range(101):
        #     banner_id = bid + 1

        #     banner = Banner(
        #         id=banner_id,
        #         title=f"Title {banner_id}",
        #         image_path=f"static/banner_img/{banner_id}.jpe",
        #         url="https://projects.ronis.info/today",
        #         visible=True,
        #         position=banner_id,
        #         created_at=datetime.datetime.utcnow(),
        #         updated_at=datetime.datetime.utcnow()
        #     )
        #     DBSession.add(banner)
