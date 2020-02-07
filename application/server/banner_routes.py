def banner_include(config):
    config.add_route('banners_view', '/')
    config.add_route('add_banner_view', '/banner/new')
    config.add_route('delete_banner_view', '/banner/{id}/delete')
    config.add_route('update_banner_view', '/banner/{id}/update')
    config.add_route('increase_banner_position_view',
                     '/banner/{id}/position/increase')
    config.add_route('decrease_banner_position_view',
                     '/banner/{id}/position/decrease')

    config.scan('.banner_views')
