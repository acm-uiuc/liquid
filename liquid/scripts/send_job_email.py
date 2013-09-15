import sys,os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ
import settings
setup_environ(settings)

from intranet.models import Job
from datetime import date
from django.core.mail import send_mail
from textwrap import wrap

def gen_email(jobs):

   today = date.today()

   email = "ACM@UIUC Weekly Job Postings\r\nWeek of " + today.strftime("%m/%d/%y") + "\r\n\r\n"
   email += "With postings from:\r\n"

   for j in jobs:
      email += "* " + j.company + "\r\n"

   email += "\r\n========================================================================\r\n\r\n";

   for j in jobs:
      email += "Title: " + j.job_title + "\r\n"
      email += "Company: " + j.company + "\r\n";
      email += "Contact: " + j.contact_name +  ' <' + j.contact_email + '> ' + j.contact_phone + "\r\n"
      email += "Hiring for: " + j.types() + "\r\n"
      description = j.description.split('\n')
      description_out = ""
      for d in description:
         if d != "":
            description_out += "\r\n".join(wrap(d,72)) + "\r\n"
      email += "Description:\r\n" + description_out + "\r\n";
      email += "\r\n========================================================================\r\n\r\n";

   return email

def send_email(addr="jobs-l@acm.illinois.edu"):
   jobs = Job.objects.filter(sent__exact=False).filter(status__exact='approve')
   if jobs:
      email = gen_email(jobs)
      try:
         send_mail('ACM@UIUC Weekly Job Postings', email, 'ACM Corporate Committee <corporate@acm.illinois.edu>',[addr], fail_silently=False)
         for j in jobs:
             j.sent = True
             j.save()
         return "Email sent to " + addr
      except Exception as inst:
         print "Error sending email"
         return "Error in sending email" + inst

   else:
      return "No jobs to send"


def view_email():
   jobs = Job.objects.filter(sent__exact=False).filter(status__exact='approve')
   if jobs:
      email = gen_email(jobs)
      return email
   else:
      return "No jobs to send"

