import sys,os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ 
import settings 
setup_environ(settings)

import csv
from intranet.models import Member

userReader = csv.reader(open(sys.argv[1],'r'))
for row in userReader:
   try:
      uid = row[4]
      netid = row[1]
      date_joined = row[5]
      if date_joined == "\\N":
         date_joined = None
      left_uiuc = row[6]
      if left_uiuc == "\\N":
         left_uiuc = None
      status = row[7]
      m = Member(uin=uid,username=netid,status=status,date_joined=date_joined,left_uiuc=left_uiuc)
      m.save()
   except:
      print "Error importing %s" % row
      pass
