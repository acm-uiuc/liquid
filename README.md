Project Liquid
==============

Project Liquid is the codename of the new ACM@UIUC website.

The master branch should always be an up to date working version of the website. Please do all
developement in a branch and merge when the feature is ready to launch.

Issues and Feature Requests
---------------------------
Please use the github issue tracker to track tasks and current work.


Getting Started
---------------
After cloning to your computer you need to have the following installed:
* mysql
  * MAC: `sudo brew install mysql`
  * Linux: `sudo apt-get install mysql-server`
* python-ldap (This is also installed from requirements.txt below)
  * MAC: `sudo pip install python-ldap` - Note: OS X formerly had problems that were solved by instructions here: http://projects.skurfer.com/posts/2011/python_ldap_lion/
  * Linux: `sudo apt-get install python-ldap`
* everything else in liquid/requirements.txt
    * This can be easily done by running 'pip install -r requirements.txt'

Run `python setup.py`

Then run the site with `python liquid/manage.py runserver`


