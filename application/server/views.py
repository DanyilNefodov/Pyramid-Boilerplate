import deform.widget
import logging
import mimetypes
import os

from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import view_config

from server.models import (
    Banner,
    DBSession, 
    Group,
    User,
    UserInGroup)
from server.schemas import BannerSchema, LoginSchema

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
    def login_form(self):
        schema = LoginSchema()
        registry = deform.widget.ResourceRegistry(self.request)
        return deform.Form(schema, buttons=('submit',), resource_registry=registry)

    @property
    def reqts(self):
        return self.banner_form.get_widget_resources()

    @view_config(route_name='banners_view', renderer='templates/banners_page.mako')
    def banners_view(self):
        banners = DBSession.query(Banner).order_by(Banner.position)

        log.debug(200)
        return dict(banners=banners, statuses=Banner.STATUSES)

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
    
    @view_config(route_name='delete_banner_view')
    def delete_banner_view(self):
        bid = int(self.request.matchdict['id'])

        banner = DBSession.query(Banner).filter_by(id=bid).first()

        if os.path.exists(banner.image_path or ""):
            os.remove(banner.image_path)

        DBSession.delete(banner)

        log.debug(201)

        url = self.request.route_url('banners_view')
        return HTTPFound(url)

    @view_config(route_name='update_banner_view', renderer='templates/add_banner_page.mako')
    def update_banner_view(self):
        bid = int(self.request.matchdict['id'])

        banner = DBSession.query(Banner).filter_by(id=bid).first()
        
        form = self.banner_form.render({
            "title": banner.title,
            # "image": image,
            "url": banner.url,
            "status": banner.status
        })

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            
            try:
                appstruct = self.banner_form.validate(controls)

            except deform.ValidationFailure as e:

                log.debug(400)
                return dict(form=e.render())
            
            new_title = appstruct.get("title", "default")
            new_url = appstruct.get("url", "default")
            new_status = int(appstruct.get("status", 0))

            img_type = mimetypes.guess_extension(appstruct.get("image").get("mimetype"))
            new_img_scr = f"static/banner_img/{banner.id}{img_type}"

            DBSession.query(Banner).filter_by(id=bid).update({
                "title": new_title,
                "image_path": new_img_scr,
                "url": new_url,
                "status": new_status
            })

            log.debug(201)

            url = self.request.route_url('banners_view')
            return HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='login_view', renderer='templates/login_page.mako')
    def login_view(self):
        form = self.login_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            
            try:
                appstruct = self.login_form.validate(controls)

            except deform.ValidationFailure as e:

                log.debug(400)
                return dict(form=e.render())

            request = self.request

            login_url = request.route_url('login_view')
            referrer = request.url
            if referrer == login_url:
                referrer = '/'

            came_from = request.params.get('came_from', referrer)

            name = appstruct.get("name")
            headers = remember(request, name)

            log.debug(201)
            return HTTPFound(location=came_from,
                             headers=headers)
        
        log.debug(200)
        return dict(form=form)

    @view_config(route_name='logout_view')
    def logout_view(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('banners_view')

        log.debug(201)
        return HTTPFound(location=url,
                         headers=headers)
    