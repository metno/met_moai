from lxml import etree
from moai.utils import XPath


class MMDContent(object):
    def __init__(self, provider):
        self.provider = provider
        self.id = None
        self.modified = None
        self.deleted = False
        self.sets = None
        self.metadata = None

    def _generate_identifier(self, path):
        return unicode(path.split('/')[-1][:-4])
        
    def update(self, path):
        self.id = self._generate_identifier(path)
        
        doc = etree.parse(path)
        ns = {'mmd': 'http://www.met.no/schema/mmd',
              'gml': 'http://www.opengis.net/gml'}
        xpath = XPath(doc, nsmap=ns)
        self.root = doc.getroot()
        
        self.modified = xpath.date('mmd:last_metadata_update')
        self.deleted = False
        self.sets = {u'public': {u'name':u'public',  u'description':u'Public access'}}

        document_text = open(path).read()
        self.metadata = {'mmd': document_text}
    