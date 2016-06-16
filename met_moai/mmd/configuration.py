import ConfigParser

config_file = 'etc/mmd_config.ini'

def get_config():
    parser = ConfigParser.SafeConfigParser()
    parser.read([config_file])
    return parser
    


def xslt_config_for(identifier):
    config = get_config()
    url = config.get(identifier, 'url')
    namespaces = config.get(identifier, 'namespaces').split(',')
    ns = {}
    for n in namespaces:
        key, value = n.split('->')
        ns[key.strip()] = value.strip()
    
    return {'url': url, 'namespaces': ns}
