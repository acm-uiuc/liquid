Production Notes
================

## Pulling in New Changes

* Log onto the production webserver using your Netid and AD Password. If you don't have access and believe you should, contact userhelp@acm.illinois.edu.
* You will need sudo access. If you don't have it, contact userhelp@acm.illinois.edu.
* Fetch the latest Docker image from the repository:

  `sudo docker pull quay.io/acmuiuc/liquid`
* Once complete, restart the Liquid service in systemd:

  `sudo systemctl restart liquid`
