import deform.widget
import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from server.models import (
    Banner,
    DBSession, 
    User)
from server.schemas import BannerSchema

from sqlalchemy import desc


log = logging.getLogger(__name__)


class Views(object):
    def __init__(self, request):
        self.request = request

    @property
    def banner_form(self):
        schema = BannerSchema()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.banner_form.get_widget_resources()

    @view_config(route_name='banners_view', renderer='templates/banners_page.mako')
    def banners_view(self):
        banners = DBSession.query(Banner).order_by(desc(Banner.position))

        log.debug(200)
        return dict(banners=banners)
    HTTPFound
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

            # Add a new page to the database
        
            # new_title = appstruct['title']
            # new_body = appstruct['body']
            # DBSession.add(Page(title=new_title, body=new_body))

            # # Get the new ID and redirect
            # page = DBSession.query(Page).filter_by(title=new_title).one()
            # new_uid = page.uid

            print(appstruct)

            url = self.request.route_url('banners_view')

            log.debug(201)
            return HTTPFound(url)

        log.debug(200)