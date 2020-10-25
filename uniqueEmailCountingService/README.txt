--------------------------------------------------------------------------------
OVERVIEW:
--------------------------------------------------------------------------------

This is an application written in python that sets up a RESTful web service. The
web service is intended to receive a JSON-formatted request of a list of emails,
and following the specifications outlined below for email matching, responds
with the number of unique emails sent in the request.

Pulling comments and information from the python code, the email counting web
service makes the following validations:

  Generally speaking, what makes a valid email address...
  name@domain.topleveldomain
   - name
     - Upper and lower characters (though treated case-insensitive)
     - Numeric characters
     - While some special characters are allowed under restrictions,
       this implementation will not consider those as invalid in any
       circumstance
   - domain.topleveldomain
     - While domains have their own series of restrictions, this
       implementation will not scrutinize those.
     - This implementation will assume the top-level domain is a valid
       one.
   - Miscellaneous rules
     - If there is a "+" in the name, anything including and after the
       "+" is ignored
     - Any "." in the name is ignored
     - For example, all of the following names equate to being relayed
       to the same email address, if on the same domain:
       - testemail
       - test.email
       - test.email+spam

--------------------------------------------------------------------------------
REQUEST SPECIFICATIONS:
--------------------------------------------------------------------------------

 - URL: http://127.0.0.1:12345/UniqueEmailCounter
 - HTTP request type: PUT
 - Content type: JSON
 - Request data format:
   {
     "emailList" : [ "email1", "email2", ... ]
   }

--------------------------------------------------------------------------------
RESPONSE SPECIFICATIONS:
--------------------------------------------------------------------------------

 - Response data format:
   {
     "numUniqueEmails" : numUniqueEmails,
     "errorText" : errorText
   }
 
 - numUniqueEmails
   - This is an integer value indicating the number of unique email addresses
     provided by the request. If there were any issues parsing the input, a
     value of -1 is returned here
 - errorText
   - If the server had no issues parsing the JSON input of the request, then
     this will indicate "Success". Otherwise, in error cases where a -1 was
     returned from numUniqueEmails, this is intended to provide more context
     about the issue (such as a lack of the emailList key).

--------------------------------------------------------------------------------
HOW TO RUN:
--------------------------------------------------------------------------------

These instructions are intended for running in a Linux environment...
You can run things by hand, or use scripts I have put in place to streamline
the process of running and testing. Both of these sets of instructions
are below.

To start either of these instructions, open a terminal in the
uniqueEmailCountingService/ directory.

 - Streamlined instructions
   - Running the web service
     - ./runUniqueEmailCountingService.sh
   - Sending a request to the web service
     - Feel free to update emails.txt file... in it, you can put email 
       addresses in, one line at a time
     - ./testUniqueEmailCountingService.sh
       - This reads in the emails.txt file and formats them in a curl call,
         according to the request specifications
 - "Running by hand" instructions
   - Running the web service
     - cd app/
     - python webservice.py
   - Sending a request to the web service
     - This can most easily be done with a curl call (as the test script does),
       of which you can extend the example, below...

       curl http://127.0.0.1:12345/UniqueEmailCounter \
         --request PUT \
         --header "Content-Type: application/json" \
         --data "{ \"emailList\" : [ \"aname@adomain.com\" ] }"

