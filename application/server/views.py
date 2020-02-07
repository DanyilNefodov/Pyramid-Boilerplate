import datetime
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
    DBSession)
from server.schemas import BannerSchema, LoginSchema
from server.utils import crop_image

from shutil import copyfile


log = logging.getLogger(__name__)


class Views(object):
    def __init__(self, request):
        self.request = request

    @property
    def banner_form(self):
        schema = BannerSchema()
        registry = deform.widget.ResourceRegistry(self.request)
        return deform.Form(schema,
                           buttons=('submit',),
                           resource_registry=registry)

    @property
    def login_form(self):
        schema = LoginSchema()
        registry = deform.widget.ResourceRegistry(self.request)
        return deform.Form(schema,
                           buttons=('submit',),
                           resource_registry=registry)

    @property
    def reqts(self):
        return self.banner_form.get_widget_resources()

    @view_config(route_name='banners_view',
                 renderer='templates/banners_page.mako')
    def banners_view(self):
        banners = DBSession.query(Banner).order_by(Banner.position)

        log.debug(200)
        return dict(banners=banners)

    @view_config(route_name='add_banner_view',
                 renderer='templates/add_banner_page.mako',
                 permission='admin')
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
            new_visible = appstruct.get("visible", True)

            new_banner = Banner(
                title=new_title,
                url=new_url,
                visible=new_visible
            )

            DBSession.add(new_banner)

            banner = DBSession.query(Banner).filter(
                Banner.title=new_title,
                Banner.url=new_url,
                Banner.visible=new_visible).order_by(Banner.id.desc()).first()

            if appstruct.get("image") is None:
                img_scr = f"static/banner_img/{banner.id}.jpg"

                copyfile(f"server/static/img/default.jpg", f"server/{img_scr}")

            else:
                img_type = mimetypes.guess_extension(
                    appstruct.get("image").get("mimetype"))
                img_scr = f"static/banner_img/{banner.id}{img_type}"

                crop_image(appstruct.get("image").get("fp"),
                           f"server/{img_scr}")

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

        banner = DBSession.query(Banner).filter(Banner.id == bid).first()

        if os.path.exists(f"server/{banner.image_path}" or ""):
            os.remove(f"server/{banner.image_path}")

        DBSession.delete(banner)

        log.debug(201)

        url = self.request.route_url('banners_view')
        return HTTPFound(url)

    @view_config(route_name='update_banner_view',
                 renderer='templates/add_banner_page.mako',
                 permission='admin')
    def update_banner_view(self):
        bid = int(self.request.matchdict['id'])

        banner = DBSession.query(Banner).filter(Banner.id == bid).first()

        form = self.banner_form.render({
            "title": banner.title,
            # "image": image,
            "url": banner.url,
            "visible": banner.visible
        })

        image_path = f"server:{banner.image_path}"

        form = form.replace('<label for="deformField2"\n         \
            class=\"control-label "\n         id="req-deformField2"\n         \
                > \\n    Image\n  </label>',
                            f'<label for="deformField2"\n         \
            class="control-label "\n         id="req-deformField2"\n         >\
                \n    Image\n  </label>\n<br><img src=\"\
                {self.request.static_url(image_path)}\" alt=\"\" \
                    draggable="false" width=200 height=200/><br>\n')

        if 'submit' in self.request.params:
            controls = self.request.POST.items()

            try:
                appstruct = self.banner_form.validate(controls)

            except deform.ValidationFailure as e:

                log.debug(400)
                return dict(form=e.render())

            new_title = appstruct.get("title", "default")
            new_url = appstruct.get("url", "default")
            new_visible = appstruct.get("visible", True)

            if appstruct.get("image") is None and not banner.image_path:
                img_scr = f"static/banner_img/{banner.id}.jpg"

                copyfile(f"server/static/img/default.jpg", f"server/{img_scr}")

            elif appstruct.get("image") is not None:
                img_type = mimetypes.guess_extension(
                    appstruct.get("image").get("mimetype"))

                img_scr = f"static/banner_img/{banner.id}{img_type}"

                crop_image(appstruct.get("image").get("fp"),
                           f"server/{img_scr}")

            else:
                img_scr = banner.image_path

            DBSession.query(Banner).filter(Banner.id == bid).update({
                "title": new_title,
                "image_path": img_scr,
                "url": new_url,
                "visible": new_visible
            })

            banner.updated_at = datetime.datetime.utcnow()

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

    @view_config(route_name='increase_banner_position_view',
                 permission='admin')
    def increase_banner_position_view(self):
        bid = int(self.request.matchdict['id'])
        cursor_banner = DBSession.query(Banner).filter(Banner.id == bid).first()

        banners = DBSession.query(Banner).order_by(Banner.position).all()

        bindex = banners.index(cursor_banner)

        if bindex != 0:
            cursor_id = banners[bindex].id
            prev_id = banners[bindex - 1].id

            cursor_position = banners[bindex].position
            prev_position = banners[bindex - 1].position

            DBSession.query(Banner).filter(Banner.id == prev_id).update({
                "position": -1
            })

            DBSession.query(Banner).filter(Banner.id == cursor_id).update({
                "position": prev_position
            })

            DBSession.query(Banner).filter(Banner.id == prev_id).update({
                "position": cursor_position
            })

            banners[bindex].updated_at = datetime.datetime.utcnow()
            banners[bindex - 1].updated_at = datetime.datetime.utcnow()

        log.debug(201)
        url = self.request.route_url('banners_view')
        return HTTPFound(url)

    @view_config(route_name='decrease_banner_position_view',
                 permission='admin')
    def decrease_banner_position_view(self):
        bid = int(self.request.matchdict['id'])
        cursor_banner = DBSession.query(Banner).filter(Banner.id == bid).first()

        banners = DBSession.query(Banner).order_by(Banner.position).all()

        bindex = banners.index(cursor_banner)

        if bindex + 1 != len(banners):
            cursor_id = banners[bindex].id
            next_id = banners[bindex + 1].id

            cursor_position = banners[bindex].position
            next_position = banners[bindex + 1].position

            DBSession.query(Banner).filter(Banner.id == next_id).update({
                "position": -1
            })

            DBSession.query(Banner).filter(Banner.id == cursor_id).update({
                "position": next_position
            })

            DBSession.query(Banner).filter(Banner.id == next_id).update({
                "position": cursor_position
            })

            banners[bindex].updated_at = datetime.datetime.utcnow()
            banners[bindex - 1].updated_at = datetime.datetime.utcnow()

        log.debug(201)
        url = self.request.route_url('banners_view')
        return HTTPFound(url)
