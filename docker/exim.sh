#!/bin/sh

EXIMHOST=${EXIMHOST-"engr-acm-web-01.acm.illinois.edu"}

debconf-set-selections <<< "exim4-config exim4/dc_other_hostnames string $EXIMHOST"
debconf-set-selections <<< "exim4-config exim4/no_config boolean true"
debconf-set-selections <<< "exim4-config exim4/hide_mailname boolean "
debconf-set-selections <<< "exim4-config exim4/use_split_config boolean false"
debconf-set-selections <<< "exim4-config exim4/dc_minimaldns boolean false"
debconf-set-selections <<< "exim4-config exim4/dc_local_interfaces string 127.0.0.1 ; ::1"
debconf-set-selections <<< "exim4-config exim4/dc_eximconfig_configtype select mail sent by smarthost; no local mail"
debconf-set-selections <<< "exim4-config exim4/no_config boolean true"
debconf-set-selections <<< "exim4-config exim4/hide_mailname boolean true"
debconf-set-selections <<< "exim4-config exim4/dc_postmaster string "
debconf-set-selections <<< "exim4-config exim4/dc_localdelivery select mbox format in /var/mail/"
debconf-set-selections <<< "exim4-config exim4/dc_smarthost string express-smtp.cites.uiuc.edu"
debconf-set-selections <<< "exim4-config exim4/dc_relay_domains string "
debconf-set-selections <<< "exim4-config exim4/dc_readhost string $EXIMHOST"
debconf-set-selections <<< "exim4-config exim4/dc_relay_nets string "
debconf-set-selections <<< "exim4-config exim4/purge_spool boolean false"
debconf-set-selections <<< "exim4-config exim4/mailname string $EXIMHOST"

apt-get install exim4
