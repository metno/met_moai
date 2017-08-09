#!/bin/bash

set -euo pipefail
IFS=$'\n\t'


apt-get update
apt-get -y install python-pip libxml2-dev libxslt-dev zlib1g-dev subversion

python setup.py install

if ! grep ^oaipmh: /etc/passwd; then
	useradd -M oaipmh
	usermod -L oaipmh
fi

for d in /var/log/met_moai /var/lib/met_moai /var/lib/met_moai/egg; do
	mkdir -p $d
	chown oaipmh:oaipmh $d
done
mkdir -p /usr/local/etc/met_moai/

cp etc/system/met_moai.service /etc/systemd/system/
cp etc/system/met_moai_update.service /etc/systemd/system/
cp etc/system/met_moai_update.timer /etc/systemd/system/

cp etc/settings.ini /usr/local/etc/met_moai/
cp etc/mmd_config.ini /usr/local/etc/met_moai/

systemctl daemon-reload

systemctl start met_moai_update.service

systemctl enable met_moai_update.timer
systemctl start met_moai_update.timer

systemctl enable met_moai.service
systemctl start met_moai.service
