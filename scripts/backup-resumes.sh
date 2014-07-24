#!/bin/bash
set -e

bucket=$1
name=$2
function usage() {
    echo "usage: $0 <bucket-name> <filename>"
    exit 1
}

if [ -z $bucket ]; then
    usage
fi
if [ -z $name ]; then
    usage
fi

tmpfile=`mktemp -t ${bucket}XXXXXX.tar.gz`

tar -czvf $tmpfile /afs/acm/project/liquid/resumes

resource="/${bucket}/${name}"
contentType="application/x-compressed-tar"
dateValue=`date -u +"%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="PUT\n\n${contentType}\n${dateValue}\n${resource}"

signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${S3_BACKUP_SECRET_KEY} -binary | base64`

curl --upload-file "$tmpfile" \
    -H "Date: ${dateValue}" \
    -H "Content-type: ${contentType}" \
    -H "Authorization: AWS ${S3_BACKUP_ACCESS_KEY}:${signature}" \
    http://s3.amazonaws.com${resource}

echo "Backup complete"
