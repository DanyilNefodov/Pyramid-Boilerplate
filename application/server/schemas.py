import colander
from colander import Invalid

import deform
import deform.widget
from deform import Form, ValidationFailure

from server.models import Banner

import validators


class MemoryTmpStore(dict):
    def preview_url(self, uid):
        return None

tmpstore = MemoryTmpStore()


def url_validator(node, value: str):
    if not validators.url(value):
        raise Invalid(node,
                    f"URL {value} is not valid")


class BannerSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    image = colander.SchemaNode(
            deform.FileData(),
            widget=deform.widget.FileUploadWidget(tmpstore)
            )
    url = colander.SchemaNode(colander.String(), validator=url_validator)
    status = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.SelectWidget(
                             values=Banner.STATUSES)
            )
