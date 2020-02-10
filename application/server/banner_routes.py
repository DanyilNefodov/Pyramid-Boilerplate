def banner_include(config):
    config.add_route('banners_view', '/')
    config.add_route('login_view', '/login')
    config.add_route('logout_view', '/logout')

    config.scan('.banner_views')
