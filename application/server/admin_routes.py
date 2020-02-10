def admin_include(config):
    config.add_route('admin_view', '/admin')
    config.add_route('admin_paginated_view', '/admin:page?={id}')
    config.add_route('add_banner_view', '/banner/new')
    config.add_route('delete_banner_view', '/banner/{id}/delete')
    config.add_route('update_banner_view', '/banner/{id}/update')
    config.add_route('increase_banner_position_view',
                     '/banner/{id}/position/increase')
    config.add_route('decrease_banner_position_view',
                     '/banner/{id}/position/decrease')

    config.scan('.admin_views')
