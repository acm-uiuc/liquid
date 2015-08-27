# -*- coding: utf-8 -*-
import re
import urllib2
from types import UnicodeType

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcall import MultipartPostHandler

import settings

from sets import Set

from django.contrib.auth.models import User

# Mailman-Messages for a successfull subscription
SUBSCRIBE_MSG = (
    u'Successfully subscribed', # en
)

# Mailman-Messages for successfully remove from a list
UNSUBSCRIBE_MSG = (
   u'Successfully Removed',
   u'Successfully Unsubscribed', # also en
)

# Mailman-Messages for a failed remove from a list
NON_MEMBER_MSG = (
    u'Cannot unsubscribe non-members', # en
)

# POST-Data for a list subcription
SUBSCRIBE_DATA = {
    'subscribe_or_invite': '0',
    'send_welcome_msg_to_this_batch': '0',
    'notification_to_list_owner': '0',
    'adminpw': None,
    'subscribees_upload': None,
}

# POST-Data for a list removal
UNSUBSCRIBE_DATA = {
    'send_unsub_ack_to_this_batch': 0,
    'send_unsub_notifications_to_list_owner': 0,
    'adminpw': None,
    'unsubscribees_upload': None,
}

def check_encoding(value, encoding):
    if isinstance(value, UnicodeType) and encoding != 'utf-8':
        value = value.encode(encoding)
    if not isinstance(value, UnicodeType) and encoding == 'utf-8':
        value = unicode(value, errors='replace')
    return value


class List(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.name)

    def __parse_status_content(self, content):
        if not content:
            raise Exception('No valid Content!')

        m = re.search('(?<=<h5>).+(?=:[ ]{0,1}</h5>)', content)
        if m:
            msg = m.group(0).rstrip()
        else:
            m = re.search('(?<=<h3><strong><font color="#ff0000" size="\+2">)'+
                          '.+(?=:[ ]{0,1}</font></strong></h3>)', content)
            if m:
                msg = m.group(0)
            else:
                raise Exception(msg) # Ace debug
                raise Exception('Could not find status message')

        m = re.search('(?<=<ul>\n<li>).+(?=\n</ul>\n)', content)
        if m:
            member = m.group(0)
        else:
            raise Exception('Could not find member-information')

        msg = msg.encode(settings.MAILMAN_ENCODING)
        member = member.encode(settings.MAILMAN_ENCODING)
        return (msg, member)

    def __parse_member_content(self, content):
        if not content:
            raise Exception('No valid Content!')
        members = []
        letters = re.findall('letter=\w{1}', content)
        chunks = re.findall('chunk=\d+', content)
        input = re.findall('name=".+_realname" type="TEXT" value=".*" size="[0-9]+" >', content)
        for member in input:
            info = member.split('" ')
            email = re.search('(?<=name=").+(?=_realname)', info[0]).group(0)
            email = unicode(email, settings.MAILMAN_ENCODING)
            members.append(email)
        letters = set(letters)
        return (letters, members, chunks)

    def __get_admin_moderation_url(self):
        return '%s/admindb/%s/?adminpw=%s' % (settings.MAILMAN_URL, self.name,
                                              settings.MAILMAN_PASSWORD)

    def __subscribe(self, email, first_name=u'', last_name=u'', send_welcome_msg=False):
        from email.Utils import formataddr

        if settings.DEBUG:
            return

        url = '%s/admin/%s/members/add' % (settings.MAILMAN_URL, self.name)

        first_name = check_encoding(first_name, settings.MAILMAN_ENCODING)
        last_name = check_encoding(last_name, settings.MAILMAN_ENCODING)
        email = check_encoding(email, settings.MAILMAN_ENCODING)
        name = '%s %s' % (first_name, last_name)

        SUBSCRIBE_DATA['adminpw'] = settings.MAILMAN_PASSWORD
        SUBSCRIBE_DATA['send_welcome_msg_to_this_batch'] = send_welcome_msg and "1" or "0"
        SUBSCRIBE_DATA['subscribees_upload'] = formataddr([name.strip(), email])
        opener = urllib2.build_opener(MultipartPostHandler(settings.MAILMAN_ENCODING, True))
        content = opener.open(url, SUBSCRIBE_DATA).read()

        (msg, member) = self.__parse_status_content(unicode(content, settings.MAILMAN_ENCODING))
        if (msg not in SUBSCRIBE_MSG):
            error = u'%s: %s' % (unicode(msg, encoding=settings.MAILMAN_ENCODING), unicode(member, encoding=settings.MAILMAN_ENCODING))
            raise Exception(error.encode(settings.MAILMAN_ENCODING))

    def __unsubscribe(self, email):
        url = '%s/admin/%s/members/remove' % (settings.MAILMAN_URL, self.name)

        email = check_encoding(email, settings.MAILMAN_ENCODING)
        UNSUBSCRIBE_DATA['adminpw'] = settings.MAILMAN_PASSWORD
        UNSUBSCRIBE_DATA['unsubscribees_upload'] = email
        opener = urllib2.build_opener(MultipartPostHandler(settings.MAILMAN_ENCODING))
        content = opener.open(url, UNSUBSCRIBE_DATA).read()

        (msg, member) = self.__parse_status_content(content)
        if (msg not in UNSUBSCRIBE_MSG) and (msg not in NON_MEMBER_MSG):
            error = u'%s: %s' % (msg, member)
            raise Exception(error.encode(settings.MAILMAN_ENCODING))

    def update_cache(self):
        url = '%s/admin/%s/members/list' % (settings.MAILMAN_URL, self.name)
        data = { 'adminpw': settings.MAILMAN_PASSWORD }
        opener = urllib2.build_opener(MultipartPostHandler(settings.MAILMAN_ENCODING))

        all_members = []
        content = opener.open(url, data).read()
        (letters, members, chunks) = self.__parse_member_content(content)
        all_members.extend(members)
        for letter in letters:
            url_letter = u"%s?%s" %(url, letter)
            content = opener.open(url_letter, data).read()
            (letters, members, chunks) = self.__parse_member_content(content)
            all_members.extend(members)
            for chunk in chunks[1:]:
                url_letter_chunk = "%s?%s&%s" %(url, letter, chunk)
                content = opener.open(url_letter_chunk, data).read()
                (letters, members, chunks) = self.__parse_member_content(content)
                all_members.extend(members)

        members = []
        for m in all_members:
            email = m.replace(u"%40", u"@")
            netid = email.split('@')[0]
            try:
               user = User.objects.get(username=netid)
               members.append(user)
            except:
               pass
        web_members = Set(members)
        db_members = Set(self.subscribers.all())
        not_in_cache = web_members.difference(db_members)
        self.subscribers.add(*not_in_cache)
        no_longer_on_web = db_members.difference(web_members)
        self.subscribers.remove(*no_longer_on_web)

    def subscribe(self,user):
       try:
         self.__subscribe(user.email, user.first_name, user.last_name, send_welcome_msg=True)
         self.subscribers.add(user)
       except:
          pass

    def subscribe_email(self,email):
        self.__subscribe(email,"","",send_welcome_msg=False)
   
    def unsubscribe(self,user):
       self.__unsubscribe(user.email)
       self.subscribers.remove(user)

    def email(self):
        return "%s@acm.uiuc.edu"%(self.name)

    
