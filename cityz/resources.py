from __future__ import absolute_import

from pyramid.traversal import find_root
from bson.objectid import ObjectId

import logging
log = logging.getLogger(__name__)


class Resource(dict):

    def __init__(self, ref, parent):
        self.__name__ = ref
        self.__parent__ = parent

    def __repr__(self):
        # use standard object representation (not dict's)
        return object.__repr__(self)
        
    def add_child(self, ref, klass):
        resource = klass(ref=ref, parent=self)
        self[ref] = resource


class MongoCollection(Resource):

    @property
    def collection(self):
        root = find_root(self)
        request = root.request
        return request.db[self.collection_name]

    def retrieve(self):
        return [elem for elem in self.collection.find()]

    def create(self, document):
        object_id = self.collection.insert(document)
        
        return self.resource_name(ref=str(object_id), parent=self)


class MongoDocument(Resource):

    def __init__(self, ref, parent):
        Resource.__init__(self, ref, parent)

        self.collection = parent.collection
        self.spec = {'_id': ObjectId(ref)}

    def retrieve(self):
        return self.collection.find_one(self.spec)

    def update(self, data, patch=False):
        if patch:
            data = {'$set': data}

        self.collection.update(self.spec, data)

    def delete(self):
        self.collection.remove(self.spec)


class City(MongoDocument):
    
    def __init__(self, ref, parent):
        MongoDocument.__init__(self, ref, parent)


class Cities(MongoCollection):
    
    collection_name = 'cities'
    resource_name = City

    def __getitem__(self, ref):
        return City(ref, self)


class Root(Resource):

    def __init__(self, request):
        Resource.__init__(self, ref='', parent=None)

        self.request = request
        self.add_child('cities', Cities)
