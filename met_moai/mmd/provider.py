import svn.remote


class SVNProvider(object):
    """Provides content from a svn mmd repository,
    implementation of :ref:`IContentProvider`"""
    
    def __init__(self, uri):
        '''
        Constructor
        '''
        self.uri = uri
        svn_url = 'https' + uri[uri.find(':'):]
        self._svn = svn.remote.RemoteClient(svn_url)
        self.elements = []
        
    def set_logger(self, log):
        """Set the logger instance for this class
        """
        self._log = log
        
    def update(self, from_date=None):
        """Harvests new content added since from_date
        returns a list of content_ids that were changed/added,
        this should be called before get_contents is called
        """
        elements = self._svn.list(extended=True)
        if from_date:
            elements = [e for e in elements if e['timestamp'] >= from_date]
        for e in elements:
            yield e['name']

    def count(self):
        """Returns number of content objects in the repository
        returns None if number is unknown, this should not be
        called before update is called
        """
        ret = 0
        for element in self.update():
            ret += 1
        return ret

    def get_content_ids(self, from_date=None):
        """returns a list/generator of content_ids
        """
        return self.update()

    def get_content_by_id(self, id):
        """Return content of a specific id
        """
        import pdb
        pdb.set_trace()
        data = self._svn.cat(id).decode('latin-1', 'ignore')
        #mmd_content = lxml.etree.fromstring(data)
        return data
