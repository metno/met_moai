import ConfigParser

config_files = ['etc/mmd_config.ini',
                '/usr/local/etc/met_moai/mmd_config.ini',
                '/etc/met_moai/mmd_config.ini']

def get_config():
    parser = ConfigParser.SafeConfigParser()
    parser.read(config_files)
    return parser

def xslt_config_for(identifier):
    config = get_config()
    url = config.get(identifier, 'url')
    schema = config.get(identifier, 'schema')
    namespaces = config.get(identifier, 'namespace')
    return {'url': url, 
            'schema': schema, 
            'namespace': namespaces}
