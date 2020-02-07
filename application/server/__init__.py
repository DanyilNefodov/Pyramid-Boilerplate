from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from server.admin_routes import admin_include
from server.banner_routes import banner_include
from server.models import DBSession, Base
from server.security import groupfinder


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings,
                          root_factory='server.resources.Root')

    config.include('pyramid_mako')
    config.include('pyramid_tm')

    authn_policy = AuthTktAuthenticationPolicy(
        settings['server.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include(admin_include, route_prefix='/')
    config.include(banner_include, route_prefix='/')

    config.add_static_view('static', 'server:static/')
    return config.make_wsgi_app()
