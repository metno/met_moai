import lxml.etree
import urllib
import logging
from met_moai.mmd.configuration import xslt_config_for
from sqlalchemy.sql.ddl import SchemaDropper


class MMDFormat(object):
    def __init__(self, prefix, config, db):
        self.prefix = prefix
        self.config = config
        self.db = db

        self.ns = {'mmd': 'http://www.met.no/schema/mmd',
                   'gml': 'http://www.opengis.net/gml'}
        self.schemas = {'mmd': 'http://www.met.no/schema/mmd'}
        
    def get_namespace(self):
        return self.ns[self.prefix]

    def get_schema_location(self):
        return self.schemas[self.prefix]
    
    @staticmethod
    def document(metadata):
        data = metadata.record
        record = metadata.record['metadata']['mmd']
        record = record.encode('utf8')
        return lxml.etree.XML(record)
    
    def __call__(self, element, metadata):
        element.append(MMDFormat.document(metadata))


class _ConvertingFormat(object):
    '''Generic converter, reading data in mmd format, and converting it using the given schema.'''
    
    xslt_location = None
    schema_location = None
    namespace = None
    
    def __init__(self, prefix, config, db):
        self.prefix = prefix
        self.config = config
    
    def get_namespace(self):
        return self.namespace

    def get_schema_location(self):
        return self.schema_location
    
    def __call__(self, element, metadata):
        doc = urllib.urlopen(self.xslt_location).read() 
        xslt_root = lxml.etree.XML(doc)
        transform = lxml.etree.XSLT(xslt_root)

        doc = MMDFormat.document(metadata)
        
        element.append(transform(doc).getroot())
        
        
def create_converter_to(identifier):
    try:
        config = xslt_config_for(identifier)
        class ReturnedFormat(_ConvertingFormat):
            xslt_location = config['url']
            schema_location = config['schema']
            namespace = config['namespace']
        return ReturnedFormat
    except KeyError:
        logging.warning('No conversion info available for ' + identifier)
        return None

ISO19115 = create_converter_to('iso19115')
