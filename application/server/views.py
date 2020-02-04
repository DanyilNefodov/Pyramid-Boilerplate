import deform.widget
import logging
import mimetypes

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from server.models import (
    Banner,
    DBSession, 
    User)
from server.schemas import BannerSchema

from sqlalchemy import desc, update


log = logging.getLogger(__name__)


class Views(object):
    def __init__(self, request):
        self.request = request

    @property
    def banner_form(self):
        schema = BannerSchema()
        registry = deform.widget.ResourceRegistry(self.request)
        return deform.Form(schema, buttons=('submit',), resource_registry=registry)

    @property
    def reqts(self):
        return self.banner_form.get_widget_resources()

    @view_config(route_name='banners_view', renderer='templates/banners_page.mako')
    def banners_view(self):
        banners = DBSession.query(Banner).order_by(desc(Banner.position))

        log.debug(200)
        return dict(banners=banners)

    @view_config(route_name='add_banner_view', renderer='templates/add_banner_page.mako')
    def add_banner_view(self):
        form = self.banner_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            
            try:
                appstruct = self.banner_form.validate(controls)

            except deform.ValidationFailure as e:

                log.debug(400)
                return dict(form=e.render())
            
            log.debug(appstruct)

            new_title = appstruct.get("title", "default")
            new_url = appstruct.get("url", "default")
            new_status = int(appstruct.get("status", 0))

            new_banner = Banner(
                title=new_title,
                url=new_url,
                status=new_status
            )

            DBSession.add(new_banner)

            banner = DBSession.query(Banner).filter_by(
                title=new_title,
                url=new_url,
                status=new_status).order_by(desc(Banner.id)).first()


            img_type = mimetypes.guess_extension(appstruct.get("image").get("mimetype"))
            img_scr = f"static/banner_img/{banner.id}{img_type}"

            with open(f"server/{img_scr}", 'wb') as f:
                f.write(appstruct.get("image").get("fp").read())

            banner.image_path = img_scr
            banner.position = banner.id

            log.debug(201)
            url = self.request.route_url('banners_view')

            return HTTPFound(url)

        log.debug(200)
        return dict(form=form)