from lxml import etree
import urllib
from datetime import datetime
import re

def parse_time(timestring):
    alternatives = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d']
    for a in alternatives:
        try:
            return datetime.strptime(timestring, a)
        except ValueError:
            pass
    raise ValueError('Unable to parse time string: ' + timestring)


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
        
    def update(self, path):
        match = re.match('(.+)#time=(.+)', path)
        if match:
            path = match.group(1)
            self.modified = parse_time(match.group(2))
        else:
            self.modified = None

        self.id = self._generate_identifier(path)

        document = urllib.urlopen(path)

        if document.getcode() in (200, None):
            root = etree.fromstring(document.read())
            parsed_time = root.xpath('mmd:last_metadata_update', namespaces=self._ns)
            if parsed_time:
                self.modified = parse_time(parsed_time[0].text)
            self.deleted = False
            self.sets = self._get_sets(root)
            self.metadata = {'mmd': etree.tostring(root)}
        else:
            if not self.modified:
                self.modified = datetime.now()
            self.deleted = True
            self.sets = {}
            self.metadata = {'mmd': ''}
