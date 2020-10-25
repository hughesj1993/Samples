# Base imports
import json
import os
import sys

# Constants
SERVICE_PATH = sys.path[0]
SERVICE_CFG = "webservice.cfg"

# Custom imports
#  -- Local CherryPy
sys.path.append(os.path.join(SERVICE_PATH, "..",  "CherryPy-18.6.0"))
import cherrypy

# The service that handles the requests...
class UniqueEmailCounterService(object):
  # Index for server base
  @cherrypy.expose
  def index(self):
    return "Use the UniqueEmailCounter address.\n"

  # The email counter servicing point
  # Expected JSON format:
  # {
  #   "emailList" : [ "email1", "email2", ... ]
  # }
  @cherrypy.expose
  @cherrypy.tools.accept(media='application/json')
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def UniqueEmailCounter(self):
    emailListKey = "emailList"
    numUniqueEmails = -1
    errorText = "Error parsing input"

    try:
      inputJson = cherrypy.request.json
      emailList = inputJson[emailListKey]
      if emailList is not None and isinstance(emailList, list):
        uniqueEmails = {}
        for email in emailList:
          validatedEmail = self.validateEmail(email)
          if validatedEmail is not None:
            # Capitalize on dictionary behavior to hold unique
            # email addresses.
            uniqueEmails[validatedEmail] = 1
        numUniqueEmails = len(uniqueEmails)
        errorText = "Success"
      else:
        errorText = 'Expected a JSON input format of ' + \
                    '{ ' + emailListKey + ' : [ email1, email2, ... ] }'
    except Exception as e:
      print("Error occurred while handling request: " + str(e))

    outputJson = {
      "numUniqueEmails" : numUniqueEmails,
      "errorText" : errorText
    }

    print("Handled UniqueEmailCounter request: " + str(outputJson))

    return outputJson

  ##
  # Determines if an email is valid or not, based on the following
  # specifications:
  #   Generally speaking, what makes a valid email address...
  #   name@domain.topleveldomain
  #    - name
  #      - Upper and lower characters (though treated case-insensitive)
  #      - Numeric characters
  #      - While some special characters are allowed under restrictions,
  #        this implementation will not consider those as invalid in any
  #        circumstance
  #    - domain.topleveldomain
  #      - While domains have their own series of restrictions, this
  #        implementation will not scrutinize those.
  #      - This implementation will assume the top-level domain is a valid
  #        one.
  #
  # Returns:
  #  - None, if the provided email does not pass validations
  #  - A lowercased, base version of the email address that will ultimately
  #    be where an email gets sent to, following Gmail account matching,
  #    if the provided email passes validations
  #    - For example, all of the following will go to the same place...
  #      - testemail@gmail.com (the base version)
  #      - test.email@gmail.com (Any "." in the name is ignored)
  #      - test.email+spam@gmail.com (anything after "+" is ignored)
  def validateEmail(self, email):
    validatedEmail = None
    valid = True

    # Sanity... make sure we actually have an email to work with, and
    # try to break it up into the separate components.
    emailSplit = None
    if email is not None:
      emailSplit = email.split("@")
    else:
      valid = False

    # Verify there's two, and only two, components... the name and domain
    name = None
    domain = None
    if valid and len(emailSplit) == 2:
      name = emailSplit[0]
      domain = emailSplit[1]
    else:
      valid = False

    # Verify the possibility of a top-level domain, by verifying at least
    # one "." in the domain portion
    if valid and len(domain.split(".", 1)) <= 1:
      valid = False

    # ... other verifications could be placed here, such as ...
    # ... top-level domain verifications, verifying special ...
    # ... character restrictions, etc.                      ...

    if valid:
      # All validations passed. Now, determine the base name
      # and return the lowercased version of it

      # Remove anything with and following a "+"
      plusIdx = name.rfind("+")
      if plusIdx != -1:
        name = name[:plusIdx]

      # Remove any "."
      name = name.replace(".", "")

      # Finally, have the name lowercased such that something like
      # "name" and "NAME" resolve to the same thing.
      name = name.lower()

      # Regenerate the address to return
      validatedEmail = "".join((name, "@", domain))

    return validatedEmail

# Main
if __name__ == "__main__":
  print("Starting...")
  cherrypy.quickstart(UniqueEmailCounterService(), "/", SERVICE_CFG)

