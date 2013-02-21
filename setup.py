import MySQLdb
import getpass 
print "Before running this script make sure that you have followed the instructions in README"
print "--Setting up liquid--"
mysql_user = raw_input('mysql username (probably root)? ')
mysql_pass = raw_input('mysql pass (probably blank)? ')

## Create the database for them
db=MySQLdb.connect(user=mysql_user,passwd=mysql_pass) 
c=db.cursor() 
try:
   c.execute('CREATE DATABASE acm_integrate')
except:
   print "!! Looks like you already have a database called 'acm_integrate'"

print "So that we can send emails from your machine we are going to use your gmail credentials:"
gmail_email = raw_input('gmail email, including @gmail.com? ')
gmail_pass = getpass.getpass("gmail password? ")

local_settings =  """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'acm_integrate',                      # Or path to database file if using sqlite3.
        'USER': '%s',                      # Not used with sqlite3.
        'PASSWORD': '%s',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
                 "init_command": "SET foreign_key_checks = 0;",
            },
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '%s'
EMAIL_HOST_PASSWORD = '%s'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MAILMAN_URL = 'https://www-s.acm.uiuc.edu/mailman/'
MAILMAN_PASSWORD = ''
MAILMAN_ENCODING = 'us-ascii'

RESUME_STORAGE_LOCATION = '' # you should set this

"""%(mysql_user,mysql_pass,gmail_email,gmail_pass)
   
FILE = open('liquid/local_settings.py',"w")
FILE.writelines(local_settings)
FILE.close()

### run all the syncing
import sys,os
sys.path.append(os.path.abspath('liquid'),),

from django.core.management import setup_environ 
import settings 
setup_environ(settings),

os.system('cd liquid; python manage.py syncdb --noinput;')
os.system('cd liquid; python manage.py migrate intranet;')
os.system('cd liquid; python manage.py migrate intranet.chroma;')

from intranet.models import Member, Group, GroupMember
from datetime import datetime

netid = raw_input('netid? ')
uin = raw_input('uin? ')

# setup mailing lists
from utils.django_mailman.models import List
t_list = List(name="top4")
m_list = List(name="Membership-l")
j_list = List(name="Jobs-l")
t_list.save()
m_list.save()
j_list.save()

m = Member(username=netid,uin=uin)
m.save()

g = Group(name='Top4',type='O',date_formed=datetime.now(), mailing_list=t_list)
g.save()
GroupMember(member=m,group=g,is_chair=True,is_admin=True).save()
