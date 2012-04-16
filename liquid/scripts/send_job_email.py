import sys,os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ 
import settings 
setup_environ(settings)

def wrap(string, width=80, ind1=0, ind2=0, prefix=''):
    """ word wrapping function.
        string: the string to wrap
        width: the column number to wrap at
        prefix: prefix each line with this string (goes before any indentation)
        ind1: number of characters to indent the first line
        ind2: number of characters to indent the rest of the lines
    """
    string = prefix + ind1 * " " + string
    newstring = ""
    while len(string) > width:
        # find position of nearest whitespace char to the left of "width"
        marker = width - 1
        while not string[marker].isspace():
            marker = marker - 1

        # remove line from original string and add it to the new string
        newline = string[0:marker] + "\n"
        newstring = newstring + newline
        string = prefix + ind2 * " " + string[marker + 1:]

    return newstring + string


from intranet.models import Job
from datetime import date

jobs = Job.objects.filter(sent__exact=False).filter(status__exact='approve')

if jobs:

   today = date.today()

   email = "ACM@UIUC Weekly Job Postings\r\nWeek of " + today.strftime("%m/%d/%y") + "\r\n\r\n"
   email += "With postings from:\r\n"

   for j in jobs:
      email += j.company + "\r\n"

   email += "\r\n========================================================================\r\n\r\n";

   for j in jobs:
      email += "Title: " + j.job_title + "\r\n"
      email += "Company: " + j.company + "\r\n";
      email += "Contact: " + j.contact_name +  ' <' + j.contact_email + '> ' + j.contact_phone + "\r\n"
      email += "Hiring for: " + j.types() + "\r\n"
      email += "Description:\r\n" + wrap(j.description, 72) + "\r\n";
      email += "\r\n========================================================================\r\n\r\n";
      j.sent = True
      j.save()


   print email
else:
   print "No jobs to send"