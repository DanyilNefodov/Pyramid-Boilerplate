import colander

import deform
import deform.widget
from deform import Form, ValidationFailure
from deform.interfaces import FileUploadTempStore 

from server.models import Banner

import validators


tmpstore = FileUploadTempStore()


class BannerSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    image = colander.SchemaNode(
            deform.FileData(),
            widget=deform.widget.FileUploadWidget(tmpstore)
            )
    url = colander.SchemaNode(colander.String())
    status = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.SelectWidget(
                             values=Banner.STATUSES)
            )

    def validator(self, node: "BannerSchema", appstruct: dict):
        
        url = appstruct.get("url", "")

        if not validators.url(url):
            raise deform.exception.ValidationFailure