#!/usr/bin/python
####
# 02/2006 Will Holcomb <wholcomb@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
"""
Usage:
  Enables the use of multipart/form-data for posting forms

Inspirations:
  Upload files in python:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
    http://odin.himinbi.org/MultipartPostHandler.py
  urllib2_file:
    Fabien Seisen: <fabien@seisen.org>

Example:
  import MultipartPostHandler, urllib2, cookielib

  cookies = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                MultipartPostHandler.MultipartPostHandler)
  params = { "username" : "bob", "password" : "riviera",
             "file" : open("filename", "rb") }
  opener.open("http://wwww.bobsite.com/upload/", params)

Further Example:
  The main function of this file is a sample which downloads a page and
  then uploads it to the W3C validator.

Updates:
  02/2009 Bernd Schlapsi:
    add support for multipart encoding
    add Parameter force_multipart
"""
import urllib
import urllib2
import mimetools, mimetypes
import os, stat
from types import UnicodeType

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1


class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def __init__(self, encoding='utf-8', force_multipart=False):
        self.encoding = encoding
        self.force_multipart = force_multipart

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0 and not self.force_multipart:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        return request

    def multipart_encode(self, vars, files, boundary = None, buffer = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
            boundary_str = u'--%s\r\n' % boundary
        if buffer is None:
            buffer = u''
        for(key, value) in vars:
            key = unicode(key, self.encoding, 'replace')
            value = unicode(str(value), self.encoding, 'replace')
            buffer += boundary_str
            buffer += u'Content-Disposition: form-data; name="%s"' % key
            buffer += u'\r\n\r\n' + value + u'\r\n'
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = os.path.basename(fd.name)
            contenttype = mimetypes.guess_type(filename)[0] or u'application/octet-stream'
            key = unicode(key, self.encoding, 'replace')
            filename = unicode(filename, self.encoding, 'replace')
            buffer += boundary_str
            buffer += u'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += u'Content-Type: %s\r\n' % contenttype
            buffer += u'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buffer += u'\r\n' + fd.read() + u'\r\n'
        buffer += boundary_str
        if self.encoding != 'utf-8':
            buffer = buffer.encode(self.encoding)

        return boundary, buffer

    https_request = http_request


def main():
    import tempfile, sys

    validatorURL = "http://validator.w3.org/check"
    opener = urllib2.build_opener(MultipartPostHandler)

    def validateFile(url):
        temp = tempfile.mkstemp(suffix=".html")
        os.write(temp[0], opener.open(url).read())
        params = { "ss" : "0",            # show source
                   "doctype" : "Inline",
                   "uploaded_file" : open(temp[1], "rb") }
        print opener.open(validatorURL, params).read()
        os.remove(temp[1])

    if len(sys.argv[1:]) > 0:
        for arg in sys.argv[1:]:
            validateFile(arg)
    else:
        validateFile("http://www.google.com")


if __name__=="__main__":
    main()