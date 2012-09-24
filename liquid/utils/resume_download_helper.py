import pyPdf
from StringIO import StringIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def generate_resume_download(people,name,generation_date,file_path):
   # Our container for 'Flowable' objects
   elements = []

   # A basic document for us to write to 'rl_hello_table.pdf'
   buffer = StringIO() 
   doc = SimpleDocTemplate(buffer,pagesize=letter)

   styles = getSampleStyleSheet()
   elements.append(Paragraph("ACM@UIUC Resume Book",styles['Title']))
   elements.append(Spacer(1, .5*inch))
   elements.append(Paragraph(name,styles['Normal']))
   elements.append(Paragraph("Generated on %s"%generation_date.strftime("%a, %d %b %Y %H:%M:%S"),styles['Normal']))
   elements.append(Spacer(1, .5*inch))


   data = [['Name','Graduation','Level','Seeking','ACM Member']]
   
   resumes = []


   for p in people:
      data.append([p.full_name(),p.get_graduation_display(),p.get_level_display(),p.get_seeking_display(),p.acm_member()])
      resumes.append(p.latest_resume().resume.path)


   # First the top row, with all the text centered and in Times-Bold,
   # and one line above, one line below.
   ts = [('ALIGN', (1,1), (-1,-1), 'LEFT'),
       ('LINEABOVE', (0,0), (-1,0), 1, colors.blue),
       ('LINEBELOW', (0,0), (-1,0), 1, colors.blue),
       ('FONT', (0,0), (-1,0), 'Times-Bold'),
       ('FONTSIZE', (0,0), (-1,-1), 8)]

   # Create the table with the necessary style, and add it to the
   # elements list.


   table = Table(data, style=ts)
   elements.append(table)


   # Write the document to disk
   doc.build(elements)


   pdf_out = pyPdf.PdfFileWriter()

   pdf_in = pyPdf.PdfFileReader(buffer)
   for page in xrange(pdf_in.getNumPages()):
      pdf_out.addPage(pdf_in.getPage(page))
   

   for r in resumes:
      pdf_in = pyPdf.PdfFileReader(file(r,"rb"))
   
      for page in xrange(pdf_in.getNumPages()):
         pdf_out.addPage(pdf_in.getPage(page))

   file_out = file(file_path, "wb")
   pdf_out.write(file_out)
   file_out.close()