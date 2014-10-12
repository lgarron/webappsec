import os

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):

        protocol = "https" if (os.environ['HTTPS'] == "on") else "http"

        hsts_message_extra = ""

        if self.request.get("hsts-max-age"):
            try:
                hsts_max_age = int(self.request.get("hsts-max-age"))
                self.response.headers['Strict-Transport-Security'] = ('max-age=%d' % hsts_max_age)
                hsts_message = ("HSTS max-age sent: %d" % hsts_max_age)
                if protocol != "https":
                    hsts_message_extra += "(NOTE: this request was not sent over HTTPS, so your browser should ignore this value.)"
                elif hsts_max_age == 0:
                    hsts_message_extra += "(max-age=0 means that HSTS should be turned off for this domain now.)"
            except Exception:
                self.response.headers['Strict-Transport-Security'] = 'invalid request'
                hsts_message = "Invalid HSTS max-age requested."
        else:
            hsts_message = "HSTS"

        template_values = {
            "protocol": protocol,
            "host": os.environ['HTTP_HOST'],
            "hsts_message": hsts_message,
            "hsts_message_extra": hsts_message_extra
        }

        template = JINJA_ENVIRONMENT.get_template('resources/templates/index.html')
        self.response.write(template.render(template_values))

class Script(webapp2.RequestHandler):

    def get(self):

        protocol = "https" if (os.environ['HTTPS'] == "on") else "http"

        template_values = {
            "protocol": protocol
        }

        template = JINJA_ENVIRONMENT.get_template('dynamic/script.js')
        self.response.write(template.render(template_values))

class Image(webapp2.RequestHandler):

    def get(self):

        protocol = "https" if (os.environ['HTTPS'] == "on") else "http"
        self.response.headers['Content-Type'] = "image/jpg"
        with file('resources/' + protocol + '/image.jpg') as f:
            source = f.read()
        self.response.write(source)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/dynamic/script.js', Script),
    ('/resources/image.jpg', Image)
], debug=True)
