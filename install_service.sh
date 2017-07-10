#!/bin/bash

set -euo pipefail
IFS=$'\n\t'


python setup.py install

if ! grep ^oaipmh: /etc/passwd; then
	useradd -M oaipmh
	usermod -L oaipmh
	usermod -s /bin/false oaipmh 
fi

for d in /var/log/met_moai /var/lib/met_moai; do
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
