from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.add_route('home', '/')
    config.add_route('cities', '/cities')
    config.add_route('city', '/cities/{name}')

    config.scan()
    return config.make_wsgi_app()
