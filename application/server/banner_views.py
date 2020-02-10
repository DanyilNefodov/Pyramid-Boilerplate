import deform.widget
import logging

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPInternalServerError)
from pyramid.security import (
    remember,
    forget)
from pyramid.view import view_config

from server.schemas import LoginSchema
from server.models import (
    Banner,
    DBSession,
    User)


log = logging.getLogger(__name__)


class Views(object):
    def __init__(self, request):
        self.request = request

    @property
    def login_form(self):
        schema = LoginSchema()
        registry = deform.widget.ResourceRegistry(self.request)
        return deform.Form(schema,
                           buttons=('submit',),
                           resource_registry=registry)

    @view_config(route_name='banners_view',
                 renderer='templates/banners_page.mako')
    def banners_view(self):
        try:
            banners = DBSession.query(Banner).filter(Banner.visible == True).order_by(Banner.position, Banner.id).limit(15)

            user = DBSession.query(User).filter(
                User.name == self.request.unauthenticated_userid).first()

            print("\n\n\n", self.request.unauthenticated_userid, "\n\n\n")
        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError()

        return dict(banners=banners, user=user)

    @view_config(route_name='login_view', renderer='templates/login_page.mako')
    def login_view(self):
        form = self.login_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()

            try:
                appstruct = self.login_form.validate(controls)

            except deform.ValidationFailure as e:
                return dict(form=e.render())

            request = self.request

            login_url = request.route_url('login_view')
            referrer = request.url
            if referrer == login_url:
                referrer = '/'

            came_from = request.params.get('came_from', referrer)

            name = appstruct.get("name")
            headers = remember(request, name)

            return HTTPFound(location=came_from,
                             headers=headers)

        log.debug(200)
        return dict(form=form)

    @view_config(route_name='logout_view')
    def logout_view(self):
        request = self.request
        headers = forget(request)

        url = request.route_url('banners_view')
        return HTTPFound(location=url,
                         headers=headers)
