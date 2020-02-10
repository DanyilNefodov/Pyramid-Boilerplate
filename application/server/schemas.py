import colander
from colander import Invalid

import deform
import deform.widget

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPInternalServerError
    )

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


search_visible_choices = ((0, "- Select -"),
            (1, "True"),
            (2, "False"))


@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token


@colander.deferred
def deferred_csrf_validator(node, kw):
    def validate_csrf(node, value):
        request = kw.get('request')
        csrf_token = request.session.get_csrf_token()
        if value != csrf_token:
            raise ValueError('Bad CSRF token')
    return validate_csrf


class CSRFSchema(colander.Schema):
    csrf = colander.SchemaNode(
        colander.String(),
        default=deferred_csrf_default,
        missing=deferred_csrf_default,
        validator=deferred_csrf_validator,
        widget=deform.widget.HiddenWidget(),
        )


def url_validator(node, value: str):
    if not validators.url(value):
        raise Invalid(node,
                      f"URL {value} is not valid")


def image_validator(node, value: str):
    width, height = get_size(value.get("fp").read())

    if width < 600 or height < 600:
        raise Invalid(node,
                      f"Image must be at least 600x600px")


class BannerSchema(CSRFSchema):
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


class BannerSearchSchema(CSRFSchema):
    title = colander.SchemaNode(colander.String(),
                                required=False,
                                missing="")
    url = colander.SchemaNode(colander.String(),
                              required=False,
                              missing="")
    visible = colander.SchemaNode(
            colander.Integer(),
            widget=deform.widget.SelectWidget(values=search_visible_choices))


def name_validator(node, value: str):
    try:
        user = DBSession.query(User).filter(User.name == value).first()

        if user is None:
            raise HTTPNotFound()

    except Exception:
        raise HTTPInternalServerError()

    if not user:
        raise Invalid(node,
                      f"User with name {value} does not exist")


class LoginSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=name_validator)
    password = colander.SchemaNode(colander.String())

    def validator(self, node, cstruct):
        name = cstruct['name']
        password = cstruct['password']

        try:
            user = DBSession.query(User).filter(User.name == name).first()

            if user is None:
                raise HTTPNotFound()

        except Exception:
            raise HTTPInternalServerError()

        if not check_password(password, user.password):
            raise Invalid(node,
                          f"Password is not correct")
