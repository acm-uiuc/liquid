from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    # Examples:
    url(r'^$','corporate.resume.views.main'),
    url(r'^student/$', redirect_to, {'url': '/corporate/resume/'}),
    url(r'^student/thanks/(?P<id>\d+)$','corporate.resume.views.student_thanks'),
    url(r'^student/referred$', 'corporate.resume.views.student_referred'),
    url(r'^student/unsubscribe$', 'corporate.resume.views.student_unsubscribe'),
    url(r'^student/thumb/(?P<id>\d+).png$', 'corporate.resume.views.thumb'),

    url(r'^recruiter/$','corporate.resume.views.recruiter'),
    url(r'^recruiter/generate/(?P<id>\d+)$','corporate.resume.views.recruiter_generate'),
    url(r'^recruiter/generate/diff/(?P<id>\d+)$','corporate.resume.views.recruiter_generate_diff'),
    url(r'^recruiter/download/(?P<id>\d+).pdf$', 'corporate.resume.views.recruiter_download_pdf'),
    url(r'^recruiter/download/diff/(?P<id>\d+).pdf$', 'corporate.resume.views.recruiter_download_pdf_diff'),
    url(r'^recruiter/browse$','corporate.resume.views.recruiter_browse'),
    url(r'^recruiter/pdf/(?P<netid>\w+).pdf$', 'corporate.resume.views.recruiter_pdf'),
    url(r'^recruiter/account$','corporate.resume.views.recruiter_account'),
    url(r'^recruiter/help$','corporate.resume.views.recruiter_help'),

    url(r'^rp$','corporate.resume.views.student_rp'),
)


 
