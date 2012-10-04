import sys,os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ 
import settings 
setup_environ(settings)

from intranet.models import PreResumePerson, Resume

from subprocess import check_call
from tempfile import NamedTemporaryFile
import pyPdf
from django.core.files import File 
import zbar
from PIL import Image

pdf_file = sys.argv[1]
pdf_in = pyPdf.PdfFileReader(file(pdf_file,"rb"))

png = NamedTemporaryFile(delete=False,suffix=".png")
png.close()

pdf_out_file = NamedTemporaryFile(delete=False,suffix=".pdf")
pdf_out_file.close()

for page in xrange(pdf_in.getNumPages()):
   check_call(["convert","-density","300","-resize", "2550x3300","-crop","600x600+1950+2700","+repage","%s[%d]"%(pdf_file,page), png.name])
   pil = Image.open(png.name).convert('L')
   width, height = pil.size
   raw = pil.tostring()
     
   # wrap image data
   image = zbar.Image(width, height, 'Y800', raw)
     
   # scan the image for barcodes
   scanner = zbar.ImageScanner()
   # configure the reader
   scanner.parse_config('enable')
   scanner.scan(image)

   number = None
   # extract results
   for symbol in image:
      number = int(symbol.data)
   try:
      person = PreResumePerson.objects.get(number=number)
      pdf_out = pyPdf.PdfFileWriter()
      pdf_out.addPage(pdf_in.getPage(page))
      file_out = file(pdf_out_file.name, "wb")
      pdf_out.write(file_out)
      file_out.close()

      resume = Resume(person=person)
      fd = open(pdf_out_file.name)
      resume.resume.save('new', File(fd))
      fd.close()
      resume.save()

      print "Success: %d: %s" % (number, person.full_name())

   except PreResumePerson.DoesNotExist:
      print "Error finding number: %d"%(number)

   # clean up
   del(image)

os.unlink(png.name)
os.unlink(pdf_out_file.name)