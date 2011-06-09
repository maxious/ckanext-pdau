import os
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes, IConfigurer


class PDEUCustomizations(SingletonPlugin):
    implements(IRoutes)
    implements(IConfigurer, inherit=True)

    def update_config(self, config):
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        our_public_dir = os.path.join(rootdir, 'ckanext', 'pdeu', 'theme', 'public')
        template_dir = os.path.join(rootdir, 'ckanext', 'pdeu', 'theme', 'templates')
        config['extra_public_paths'] = ','.join([our_public_dir,
                config.get('extra_public_paths', '')])
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])
        config['ckan.site_logo'] = '/img/logo.png'

    def before_map(self, route_map):
        wire_controller = 'ckanext.pdeu.controllers:RewiringController'
        route_map.connect('/tag/{tags}', controller=wire_controller,
                          action='tag')

        subscribe_controller = 'ckanext.pdeu.controllers:SubscribeController'
        route_map.connect('/subscribe',
                          controller=subscribe_controller,
                          conditions=dict(method=['POST']),
                          action='send')

        map_controller = 'ckanext.pdeu.controllers:MapController'
        route_map.connect('/map',
                          controller=map_controller,
                          action='show')

        route_map.connect('/map/data.json',
                          controller=map_controller,
                          action='data')

        return route_map

    def after_map(self, route_map):
        return route_map

