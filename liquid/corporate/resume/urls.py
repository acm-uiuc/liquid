from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^student/$','corporate.resume.views.student'),
    url(r'^student/thanks/$','corporate.resume.views.student_thanks'),
)


 