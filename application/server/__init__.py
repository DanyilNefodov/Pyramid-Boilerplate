from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession, Base

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings,
                          root_factory='server.models.Root')
    config.include('pyramid_mako')
    config.include('pyramid_tm')
    config.add_route('banners_view', '/')
    config.add_route('add_banner_view', '/add_banner/')
    config.add_route('delete_banner_view', '/delete_banner/{id}/')
    config.add_route('update_banner_view', '/update_banner/{id}/')
    config.add_static_view('static', 'server:static/')
    config.scan('.views')
    return config.make_wsgi_app()