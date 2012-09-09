from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^student/$','corporate.resume.views.student'),
    url(r'^student/thanks/(?P<id>\d+)$','corporate.resume.views.student_thanks'),

    url(r'^recruiter/$','corporate.resume.views.recruiter'),
    url(r'^recruiter/generate/(?P<id>\d+)$','corporate.resume.views.recruiter_generate'),
    url(r'^recruiter/download/(?P<id>\d+).pdf$', 'corporate.resume.views.recruiter_download_pdf'),
    url(r'^recruiter/browse$','corporate.resume.views.recruiter_browse'),
    url(r'^recruiter/pdf/(?P<netid>\w+).pdf$', 'corporate.resume.views.recruiter_pdf'),
)


 