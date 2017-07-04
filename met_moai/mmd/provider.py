import datetime
import json
import urllib2


class MetaEditProvider(object):
    """Provides content from a metadata editor web interface,
    implementation of :ref:`IContentProvider`"""
    
    def __init__(self, base_url='metadata:http://metaedit.met.no/metadataeditor/service/metaedit_api/'):
        self._base_url = base_url[base_url.find(':') + 1:]
        while self._base_url.endswith('/'):
            self._base_url = self._base_url[:-1]
        self._elements = {}
        self._project = 'met-master'
         
    def set_logger(self, log):
        """Set the logger instance for this class
        """
        self._log = log
        
    def _modified_since(self, resource, from_time):
        return from_time is None or from_time < datetime.datetime.fromtimestamp(resource['lastModified'] / 1000)
        
    def update(self, from_date=None):
        """Harvests new content added since from_date
        returns a list of content_ids that were changed/added,
        this should be called before get_contents is called
        """
        new = []
        elements = {}

        list_url = '%s/list/%s' % (self._base_url, self._project)
        resources = json.load(urllib2.urlopen(list_url))
        
        for resource in resources['records']:
            resource_name = resource['name']
            if resource_name.endswith('xml'):
                resource_name = resource_name[:-4]
            elements[resource_name] = resource
            if self._modified_since(resource, from_date):
                new.append(resource_name)
        self._elements = elements
        return new

    def count(self):
        """Returns number of content objects in the repository
        returns None if number is unknown, this should not be
        called before update is called
        """
        return len(self._elements)

    def get_content_ids(self, from_date=None):
        """returns a list/generator of content_ids
        """
        for name, resource in self._elements.items():
            if self._modified_since(resource, from_date):
                yield name

    def get_content_by_id(self, id):
        """Return content of a specific id
        """
        read_url = '%s/%s/%s' % (self._base_url, self._project, id)

        element = self._elements[id]
        return {'id': id,
                'url': read_url,
                'modified': datetime.datetime.fromtimestamp(element['lastModified'] / 1000),
                'deleted': False
                }


if __name__ == '__main__':
    import datetime
    mep = MetaEditProvider()
    print mep.update()
    print mep.update(datetime.datetime.now())
    print mep.get_content_by_id(mep._elements.keys()[0])
