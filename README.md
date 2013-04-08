Project Liquid
==============

Project Liquid is the codename of the new ACM@UIUC website.

The master branch should always be an up to date working version of the website. Please do all
developement in a branch and merge when the feature is ready to launch.

Issues and Feature Requests
---------------------------
Please use the github issues and check the trello for current work.
https://trello.com/board/acm-liquid/50511d5a1a60a3496d1d539c


Getting Started
---------------
After cloning to your computer you need to have the following installed:
* mysql
  * MAC: `sudo brew install mysql`
  * Linux: `sudo apt-get install mysql-server`
* python-ldap (This is also installed from dependencies.txt below)
  * MAC: `sudo pip install python-ldap` - Note: OS X formerly had problems that were solved by instructions here: http://projects.skurfer.com/posts/2011/python_ldap_lion/
  * Linux: `sudo apt-get install python-ldap`
* everything else in liquid/dependencies.txt


Run `python setup.py`

Then, to run the site with `python liquid/manage.py runserver`


