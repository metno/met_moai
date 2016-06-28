from lxml import etree
import urllib
import met_moai.mmd.util as util


class MMDContent(object):
    def __init__(self, provider):
        self.provider = provider
        self.id = None
        self.modified = None
        self.deleted = False
        self.sets = None
        self.metadata = None
        self._ns = {'mmd': 'http://www.met.no/schema/mmd',
              'gml': 'http://www.opengis.net/gml'}

    def _generate_identifier(self, path):
        return unicode(path.split('/')[-1][:-4])

    def _get_sets(self, root):
        ret = {}
        for element in root.xpath('mmd:keywords/mmd:keyword', namespaces=self._ns):
            if element.text is not None:
                text = unicode(element.text.replace(' > ', ':'))
                ret[text] = {u'name': text,  u'description': text}
        return ret
        
    def update(self, data):
        self.id = unicode(data['id'])
        svninfo = data['svn']
        self.modified = svninfo.date
        self.deleted = svninfo.deleted
        if not svninfo.deleted:
            document = urllib.urlopen(svninfo.path)
            root = etree.fromstring(document.read())
            parsed_time = root.xpath('mmd:last_metadata_update', namespaces=self._ns)
            if parsed_time:
                self.modified = util.parse_time(parsed_time[0].text)
            self.sets = self._get_sets(root)
            self.metadata = {'mmd': etree.tostring(root)}
        else:
            self.sets = {}
            self.metadata = {'mmd': ''}
