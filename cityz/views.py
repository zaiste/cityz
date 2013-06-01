from pyramid.view import view_config

CITIES = {
    'paris': {
        'name': 'Paris',
        'population': '2,234,105'
    },
    'sf': {
        'name': 'San Francisco',
        'population': '812,826'
    }
}

@view_config(route_name='home', renderer='json')
def home(request):
    return { 'project': 'cityz' }

@view_config(route_name='city', renderer='json')
def get_city(request):
    name = request.matchdict['name']
    return CITIES[name]

@view_config(route_name='cities', renderer='json')
def list_cities(request):
    return CITIES
