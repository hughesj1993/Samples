#!/bin/bash

DIR_PATH=`dirname $0`

source $DIR_PATH/findPython

EMAILS_TXT=emails.txt

# Build email list
echo "-----------------------------------------------"
echo "Building email list..."
echo "-----------------------------------------------"
EMAIL_LIST=""
for EMAIL in `cat $DIR_PATH/emails.txt`; do
  if [[ ! -z $EMAIL_LIST ]]; then
    EMAIL_LIST=$EMAIL_LIST,
  fi
  EMAIL_LIST=$EMAIL_LIST"\"$EMAIL\""
done

# Send the request
echo "-----------------------------------------------"
echo "Sending request..."
echo "-----------------------------------------------"
curl -s \
  http://127.0.0.1:12345/UniqueEmailCounter \
  --request PUT \
  --header "Content-Type: application/json" \
  --data "{ \"emailList\" : [ ${EMAIL_LIST} ] }" | ${PYTHON} -m json.tool

echo # newline

