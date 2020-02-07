import colander
from colander import Invalid

import deform
import deform.widget

from server.models import (
    DBSession,
    User
)
from server.password_utils import check_password
from server.utils import get_size
import validators


class MemoryTmpStore(dict):
    def preview_url(self, uid):
        return None


tmpstore = MemoryTmpStore()


def url_validator(node, value: str):
    if not validators.url(value):
        raise Invalid(node,
                      f"URL {value} is not valid")


def image_validator(node, value: str):
    width, height = get_size(value.get("fp").read())

    if width < 600 or height < 600:
        raise Invalid(node,
                      f"Image must be at least 600x600px")


class BannerSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    image = colander.SchemaNode(
            deform.FileData(),
            widget=deform.widget.FileUploadWidget(tmpstore),
            validator=image_validator,
            missing=None
            )

    url = colander.SchemaNode(colander.String(), validator=url_validator)
    visible = colander.SchemaNode(
            colander.Boolean(),
            widget=deform.widget.CheckboxWidget(),
            default=True
            )


def name_validator(node, value: str):
    user = DBSession.query(User).filter(User.name == value).first()
    print(node, flush=True)

    if not user:
        raise Invalid(node,
                      f"User with name {value} does not exist")


class LoginSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=name_validator)
    password = colander.SchemaNode(colander.String())

    def validator(self, node, cstruct):
        name = cstruct['name']
        password = cstruct['password']

        user = DBSession.query(User).filter(User.name == name).first()

        if not check_password(password, user.password):
            raise Invalid(node,
                          f"Password is not correct")
