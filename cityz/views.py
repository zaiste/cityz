import json

from pyramid.view import forbidden_view_config, notfound_view_config
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from cityz.resources import Root, Cities, City

import logging
log = logging.getLogger(__name__)

@view_config(renderer='json', context=Root)
def home(context, request):
    return {'info': 'City API'}


@view_config(request_method='GET', context=City, renderer='json')
def get_city(context, request):
    r = context.retrieve()

    if r is None:
        raise HTTPNotFound()
    else:
        return r


@view_config(request_method='DELETE', context=City, renderer='json')
def delete_city(context, request):
    context.delete()

    return Response(
        status='202 Accepted',
        content_type='application/json; charset=UTF-8')


@view_config(request_method='POST', context=Cities, renderer='json')
def create_city(context, request):
    context.create(request.json_body)

    return Response(
        status='201 Created',
        content_type='application/json; charset=UTF-8')


@view_config(request_method='PUT', context=City, renderer='json')
def update_city(context, request):
    context.update(request.json_body, True)

    return Response(
        status='202 Accepted',
        content_type='application/json; charset=UTF-8')


@view_config(request_method='GET', context=Cities, renderer='json')
def list_cities(context, request):
    return context.retrieve()


@notfound_view_config()
def notfound(request):
    return Response(
        body=json.dumps({'message': 'Custom `Not Found` message'}),
        status='404 Not Found',
        content_type='application/json')

@forbidden_view_config()
def forbidden(request):
    return Response(
        body=json.dumps({'message': 'Custom `Unauthorized` message'}),
        status='401 Unauthorized',
        content_type='application/json')

