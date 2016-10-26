# met_moai

met.no's extension for moai (https://github.com/infrae/moai), allowing the exposure of our metadata in various other formats.

## Setup and running

In met.no, you can ask team-punkt for a chef recipe, making setup very easy. 

To set up and run manually:

From top source directory:

$ virtualenv deps
$ . deps/bin/activate
$ python setup.py develop

Update etc/mmd_config.ini and etc/settings.ini

$ bin/update.sh
$ bin/run.sh

Metadata updates are in this setup not automatic. You must preiodically run bin/update.sh to get recent updates.

For running after the first time:

$ . deps/bin/activate
$ bin/run.sh

Data should then be available in your browser like this http://localhost:8080/oai?verb=ListMetadataFormats


