import getpass
import sys,os
from datetime import datetime
from django.core.management import setup_environ

sys.path.append(os.path.abspath('app'),),

import settings
setup_environ(settings),

from intranet.models import Member, Group, GroupMember
from utils.django_mailman.models import List

netid = raw_input('netid? ')
uin = raw_input('uin? ')
acct_pass = getpass.getpass("account password? ")

# setup mailing lists

t_list = List(name="top4")
m_list = List(name="Membership-l")
j_list = List(name="Jobs-l")
t_list.save()
m_list.save()
j_list.save()

m = Member(username=netid,uin=uin)
m.set_password(acct_pass)
m.save()

g = Group(name='Top4',type='O',date_formed=datetime.now(), mailing_list=t_list)
g.save()
gm = GroupMember(member=m,group=g,is_chair=True,is_admin=True)
gm.save()
