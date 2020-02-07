def admin_include(config):
    config.add_route('login_view', '/login')
    config.add_route('logout_view', '/logout')
    config.add_route('admin_view', '/admin')

    config.scan('.admin_views')
