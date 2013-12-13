from pyramid.config import Configurator
from pyramid.renderers import JSON

from cityz.resources import Root

from bson import json_util
import json

class MongoJSONRenderer: 
    def __init__(self, info): 
        pass

    def __call__(self, value, system): 
        request = system.get('request') 
        if request is not None: 
            if not hasattr(request, 'response_content_type'): 
                request.response_content_type = 'application/json' 
        return json.dumps(value, default=json_util.default) 


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    config.add_renderer('json', MongoJSONRenderer) 
    config.include('.db')
    config.scan('.views')

    return config.make_wsgi_app()
