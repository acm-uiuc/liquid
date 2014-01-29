from intranet.models import ResumePerson
import uuid

objects = ResumePerson.objects.all()

if True:
   for o in objects:
      #o.resume_uuid = uuid.uuid4()
      print o.netid
      print o.resume_uuid
      #o.save()

if True:
   o = ResumePerson.objects.get(netid__exact='nassri2')
   print o.netid
   print o.resume_uuid
