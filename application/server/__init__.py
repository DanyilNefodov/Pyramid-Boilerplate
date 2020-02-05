from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from sqlalchemy import engine_from_config

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

    config.add_route('banners_view', '/')
    config.add_route('add_banner_view', '/add_banner')
    config.add_route('delete_banner_view', '/delete_banner/{id}')
    config.add_route('update_banner_view', '/update_banner/{id}')
    config.add_route('login_view', '/login')
    config.add_route('logout_view', '/logout')
    config.add_route('increase_banner_position_view', '/increase_banner_position/{id}')
    config.add_route('decrease_banner_position_view', '/decrease_banner_position/{id}')
    config.add_static_view('static', 'server:static/')

    config.scan('.views')
    return config.make_wsgi_app()