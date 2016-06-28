import subprocess
from lxml import etree
from urlparse import urlparse
import logging
import collections
import os
import met_moai.mmd.util as util


class SubversionClient(object):
    def __init__(self, uri, svn_binary='svn'):
        if uri[-1] != '/':
            uri += '/'
        self._uri = uri
        self._svn_binary = svn_binary
        self.repository_root = self._get_repository_root(uri)
        if not uri.startswith(self.repository_root):
            raise Exception('Error when parsing subversion URI')
        self.repository_path = uri[len(self.repository_root):]

    def _full_path(self, relative_path):
        return self.repository_root + relative_path

    def _is_relevant_path(self, path):
        return path.get('kind') == 'file' and \
            path.text.endswith('.xml') and \
            path.text.startswith(self.repository_path)
            
    def _get_repository_root(self, uri):
        cmd = [self._svn_binary, 'info', '--xml', uri]
        xml = subprocess.check_output(cmd)
        root_element = etree.fromstring(xml).xpath('entry/repository/root')
        if root_element:
            return root_element[0].text
        else:
            raise Exception('Unable to parse repository root')

    def changes(self, since = None):
        cmd = [self._svn_binary, 'log', '-v', '--xml', self.repository_root]
        if since:
            cmd = cmd + ['-r', '{%s}:HEAD' % (since.isoformat(),)]
        try:
            xml = subprocess.check_output(cmd)
            root = etree.fromstring(xml)
            Entry = collections.namedtuple('LogEntry', ['date', 'msg', 'author', 'path', 'deleted'])
            entry_list = {}
            for logentry in root:  # Subversion log returns the most recent entry at starting time, but we want changes after the starting time 
                if logentry.tag != 'logentry':
                    continue
                date = util.parse_time(logentry.xpath('date')[0].text)
                msg = logentry.xpath('msg')[0].text
                author = logentry.xpath('author')[0].text
                for path in logentry.xpath('paths/path'):
                    if self._is_relevant_path(path):
                        full_path = self._full_path(path.text)
                        if not full_path in entry_list:
                            entry_list[full_path] = Entry(date, msg, author, self._full_path(path.text), path.get('action') == 'D')
            return entry_list.values()
        except subprocess.CalledProcessError as e:
            logging.error(e.output)
            raise  # TODO improve this


class SVNProvider(object):
    """Provides content from a svn mmd repository,
    implementation of :ref:`IContentProvider`"""
    
    def __init__(self, uri):
        '''
        Constructor
        '''
        svn_uri = 'https' + uri[uri.find(':'):]
        self._client = SubversionClient(svn_uri)
        self._elements = {}
        
    def set_logger(self, log):
        """Set the logger instance for this class
        """
        self._log = log
        
    def _identifier(self, uri):
        return os.path.splitext(os.path.basename(uri))[0]

    def update(self, from_date=None):
        """Harvests new content added since from_date
        returns a list of content_ids that were changed/added,
        this should be called before get_contents is called
        """
        new_modifications = {}
        modified = self._client.changes(from_date)
        for pathinfo in modified:
            id = self._identifier(pathinfo.path)
            info = {'id': id,
                    'uri': pathinfo.path,
                    'svn': pathinfo}
            new_modifications[id] = info
        self._elements.update(new_modifications)
        return new_modifications.keys()

    def count(self):
        """Returns number of content objects in the repository
        returns None if number is unknown, this should not be
        called before update is called
        """
        return len(self._elements)

    def get_content_ids(self, from_date=None):
        """returns a list/generator of content_ids
        """
        return self._elements.keys()

    def get_content_by_id(self, id):
        """Return content of a specific id
        """
        return self._elements[id]
