from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'corporate.views.main'),
    url(r'^job/$', 'corporate.views.job'),
    url(r'^job/thanks/$', 'corporate.views.thanks'),
    url(r'^resume/student/$','corporate.views.resume_student'),
    url(r'^resume/student/thanks/$','corporate.views.resume_student_thanks'),
)


 