import datetime
import deform.widget
import mimetypes
import os

from pyramid.csrf import check_csrf_token
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPInternalServerError,
    HTTPBadRequest)
from pyramid.view import view_config

from server.banner_views import log
from server.schemas import (
    BannerSchema,
    BannerSearchSchema)
from server.models import (
    Banner,
    DBSession)
from server.utils import (
    crop_image,
    filter_banners_by_search)


class Views(object):
    def __init__(self, request):
        self.request = request
        self.PAGINATION_LIMIT = 15

    @property
    def banner_form(self):
        schema = BannerSchema().bind(request=self.request)
        registry = deform.widget.ResourceRegistry(self.request)

        return deform.Form(schema,
                           buttons=('submit',),
                           resource_registry=registry)

    @property
    def banner_search_form(self):
        schema = BannerSearchSchema().bind(request=self.request)
        registry = deform.widget.ResourceRegistry(self.request)

        return deform.Form(schema,
                           buttons=('search',),
                           resource_registry=registry)

    @view_config(route_name='sort_admin_view')
    def sort_admin_view(self):
        new_column = self.request.matchdict['column']

        try:
            column = self.request.session["search_request"]["column"]

            if new_column == column:
                sort = self.request.session["search_request"]["sort"]

                if sort == "asc":
                    self.request.session["search_request"]["sort"] = "desc"
                else:
                    self.request.session["search_request"]["sort"] = "asc"
            else:
                self.request.session["search_request"]["column"] = new_column
                self.request.session["search_request"]["sort"] = "asc"

        except KeyError:
            self.request.session["search_request"]["column"] = "position"
            self.request.session["search_request"]["sort"] = "asc"

        url = self.request.route_url('admin_view')
        return HTTPFound(location=url)

    @view_config(route_name='admin_view',
                 renderer='templates/admin_page.mako')
    def admin_view(self):
        form = self.banner_search_form.render()

        # try:
        search_request = self.request.session["search_request"]
        sort = self.request.session["search_request"]["sort"]
        column = self.request.session["search_request"]["column"]

        # except KeyError:
        #     sort = "asc"
        #     column = "position"

        search_request = self.request.session["search_request"] = {
            "sort": sort,
            "column": column
        }

        print("\n\n\n", search_request, "\n\n\n")

        form = self.banner_search_form.render(search_request)

        try:
            banners = filter_banners_by_search(search_request)

            if 'search' in self.request.params:
                controls = self.request.POST.items()

                try:
                    appstruct = self.banner_search_form.validate(controls)

                    search_title = appstruct.get("title", "default")
                    search_url = appstruct.get("url", "default")
                    search_visible = appstruct.get("visible", 0)

                    search_request = self.request.session["search_request"] = {
                        "sort": sort,
                        "column": column,
                        "title": search_title,
                        "url": search_url,
                        "visible": search_visible
                    }

                    form = self.banner_search_form.render(search_request)

                    banners = filter_banners_by_search(search_request)

                except deform.ValidationFailure as e:
                    form = e.render()

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError()

        banners_count = banners.count()

        count = banners_count // self.PAGINATION_LIMIT

        if banners_count % self.PAGINATION_LIMIT != 0:
            count += 1

        return dict(form=form, banners=banners.limit(self.PAGINATION_LIMIT), page=dict(count=count, page=1))

    @view_config(route_name='admin_paginated_view',
                 renderer='templates/admin_page.mako')
    def admin_paginated_view(self):
        page = int(self.request.matchdict['id'])

        if page is None:
            raise HTTPNotFound

        sort = self.request.headers.get("sort", "asc")
        column = self.request.headers.get("columnName", "position")

        try:
            search_request = self.request.session["search_request"]
        except KeyError:
            search_request = self.request.session["search_request"] = {
                "sort": sort,
                "column": column
            }

        form = self.banner_search_form.render(search_request)

        try:
            banners = filter_banners_by_search(search_request)

            if 'search' in self.request.params:
                controls = self.request.POST.items()

                try:
                    appstruct = self.banner_search_form.validate(controls)

                    search_title = appstruct.get("title", "default")
                    search_url = appstruct.get("url", "default")
                    search_visible = appstruct.get("visible", 0)

                    search_request = self.request.session["search_request"] = {
                        "sort": sort,
                        "column": column,
                        "title": search_title,
                        "url": search_url,
                        "visible": search_visible
                    }

                    form = self.banner_search_form.render(search_request)

                    banners = filter_banners_by_search(search_request)

                except deform.ValidationFailure as e:
                    form = e.render()

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError()

        pagination_offset = self.PAGINATION_LIMIT * (page - 1)

        banners_count = banners.count()

        count = banners_count // self.PAGINATION_LIMIT

        if banners_count % self.PAGINATION_LIMIT != 0:
            count += 1

        return dict(form=form, banners=banners.offset(pagination_offset).limit(self.PAGINATION_LIMIT), page=dict(count=count, page=page))

    @view_config(route_name='add_banner_view',
                 renderer='templates/banner_edit.mako',
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

            try:
                DBSession.add(new_banner)

                banner = DBSession.query(Banner).filter(
                    Banner.title == new_title,
                    Banner.url == new_url,
                    Banner.visible == new_visible).order_by(Banner.id.desc()).first()

                if appstruct.get("image") is None:
                    img_scr = ""

                else:
                    img_type = mimetypes.guess_extension(
                        appstruct.get("image").get("mimetype"))
                    img_scr = f"static/banner_img/{banner.id}{img_type}"

                    crop_image(appstruct.get("image").get("fp"), banner.id, img_type)

                banner.image_path = img_scr
                banner.position = banner.id

                url = self.request.route_url('admin_view')
                return HTTPFound(url)

            except Exception as e:
                log.debug(e)
                raise HTTPInternalServerError()

        log.debug(200)
        return dict(form=form)

    @view_config(route_name='delete_banner_view')
    def delete_banner_view(self):
        if not check_csrf_token(self.request):
            raise HTTPBadRequest

        bid = int(self.request.matchdict['id'])

        if bid is None:
            raise HTTPNotFound

        try:
            banner = DBSession.query(Banner).filter(Banner.id == bid).first()

            if banner is None:
                raise HTTPNotFound

            if os.path.exists(f"server/{banner.image_path}" or ""):
                os.remove(f"server/{banner.image_path}")

            DBSession.delete(banner)

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError

        url = self.request.route_url('admin_view')
        return HTTPFound(url)

    @view_config(route_name='update_banner_view',
                 renderer='templates/banner_edit.mako',
                 permission='admin')
    def update_banner_view(self):
        bid = int(self.request.matchdict['id'])

        if bid is None:
            raise HTTPNotFound

        try:
            banner = DBSession.query(Banner).filter(Banner.id == bid).first()

            if banner is None:
                raise HTTPNotFound

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError

        form = self.banner_form.render({
            "title": banner.title,
            # "image": image,
            "url": banner.url,
            "visible": banner.visible
        })

        image_path = f"server:{banner.image_path}"

        try:
            form = form.replace('<label for="deformField2"\n         ' +
                'class=\"control-label "\n         id="req-deformField2"\n         ' +
                    '> \\n    Image\n  </label>',
                                f'<label for="deformField2"\n         \
                class="control-label "\n         id="req-deformField2"\n         >\
                    \n    Image\n  </label>\n<br><img src=\"\
                    {self.request.static_url(image_path)}\" alt=\"\" \
                        draggable="false" width=200 height=200/><br>\n')

        except ValueError:
            pass

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError

        if 'submit' in self.request.params:
            controls = self.request.POST.items()

            try:
                appstruct = self.banner_form.validate(controls)

            except deform.ValidationFailure as ve:
                return dict(form=ve.render())

            new_title = appstruct.get("title", "default")
            new_url = appstruct.get("url", "default")
            new_visible = appstruct.get("visible", True)

            if appstruct.get("image") is None and not banner.image_path:
                img_scr = ""

            elif appstruct.get("image") is not None:
                img_type = mimetypes.guess_extension(
                    appstruct.get("image").get("mimetype"))

                img_scr = f"static/banner_img/{banner.id}{img_type}"

                crop_image(appstruct.get("image").get("fp"), banner.id, img_type)

            else:
                img_scr = banner.image_path

            try:
                banner.title = new_title
                banner.image_path = img_scr
                banner.url = new_url
                banner.visible = new_visible
                banner.updated_at = datetime.datetime.utcnow()

            except Exception as e:
                log.debug(e)
                raise HTTPInternalServerError

            url = self.request.route_url('admin_view')
            return HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='increase_banner_position_view',
                 permission='admin')
    def increase_banner_position_view(self):
        if not check_csrf_token(self.request):
            raise HTTPBadRequest

        bid = int(self.request.matchdict['id'])

        if bid is None:
            raise HTTPNotFound

        try:
            cursor_banner = DBSession.query(Banner).filter(Banner.id == bid).first()

            if cursor_banner is None:
                raise HTTPNotFound

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError

        try:
            banners = DBSession.query(Banner).order_by(Banner.position, Banner.id).all()

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError

        bindex = banners.index(cursor_banner)

        if bindex != 0:
            cursor_position = banners[bindex].position

            try:
                banners[bindex].position = banners[bindex - 1].position
                banners[bindex].updated_at = datetime.datetime.utcnow()

                banners[bindex - 1].position = cursor_position
                banners[bindex - 1].updated_at = datetime.datetime.utcnow()

            except Exception as e:
                log.debug(e)
                raise HTTPInternalServerError

        log.debug(201)
        url = self.request.route_url('admin_view')
        return HTTPFound(url)

    @view_config(route_name='decrease_banner_position_view',
                 permission='admin')
    def decrease_banner_position_view(self):
        if not check_csrf_token(self.request):
            raise HTTPBadRequest

        bid = int(self.request.matchdict['id'])

        if bid is None:
            raise HTTPNotFound

        try:
            cursor_banner = DBSession.query(Banner).filter(Banner.id == bid).first()

            if cursor_banner is None:
                raise HTTPNotFound

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError

        try:
            banners = DBSession.query(Banner).order_by(Banner.position, Banner.id).all()

        except Exception as e:
            log.debug(e)
            raise HTTPInternalServerError

        bindex = banners.index(cursor_banner)

        if bindex + 1 != len(banners):
            cursor_position = banners[bindex].position

            try:
                banners[bindex].position = banners[bindex + 1].position
                banners[bindex].updated_at = datetime.datetime.utcnow()

                banners[bindex + 1].position = cursor_position
                banners[bindex + 1].updated_at = datetime.datetime.utcnow()

            except Exception as e:
                log.debug(e)
                raise HTTPInternalServerError

        log.debug(201)
        url = self.request.route_url('admin_view')
        return HTTPFound(url)
