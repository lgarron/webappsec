import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):

        server_url = app_identity.get_default_version_hostname()

        protocol = "https" if (os.environ['HTTPS'] == "on") else "http"

        if self.request.get("hsts-max-age"):
            try:
                hsts_max_age = int(self.request.get("hsts-max-age"))
                self.response.headers['Strict-Transport-Security'] = ('max-age=%d' % hsts_max_age)
                hsts_message = ("HSTS max-age sent: %d" % hsts_max_age)
            except Exception:
                self.response.headers['Strict-Transport-Security'] = 'invalid request'
                hsts_message = "Invalid HSTS max-age requested."
        else:
            hsts_message = "HSTS"

        template_values = {
            "protocol": protocol,
            "host": os.environ['HTTP_HOST'],
            "hsts_message": hsts_message
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Script(webapp2.RequestHandler):

    def get(self):

        server_url = app_identity.get_default_version_hostname()

        protocol = "https" if (os.environ['HTTPS'] == "on") else "http"

        template_values = {
            "protocol": protocol
        }

        if os.environ['HTTP_HOST'].startswith("hsts."):
            self.response.headers['Strict-Transport-Security'] = 'max-age=300'

        template = JINJA_ENVIRONMENT.get_template('dynamic/script.js')
        self.response.write(template.render(template_values))



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/dynamic/script.js', Script)
], debug=True)
