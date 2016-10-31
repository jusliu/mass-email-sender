import jinja2, datetime
import webapp2, os
from emails import sendEmails

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class BaseHandler(webapp2.RequestHandler):
	def render_template(self, view_filename, params=None):
		if not params:
			params = {}
		template = JINJA_ENVIRONMENT.get_template(view_filename)

		params['botcurtime'] = str(datetime.datetime.utcnow())
		self = addResponseHeaders(self)
		self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
	def get(self):
		self.render_template('templates/home.html')

class AboutHandler(BaseHandler):
	def get(self):
		self.render_template('templates/about.html')

class ProductHandler(BaseHandler):
	def get(self):
		self.render_template('templates/product.html')

class ResultsHandler(BaseHandler):
	def post(self):
		self = addResponseHeaders(self)
		email_subject = self.request.get('email-subject')
		email_template = self.request.get('email-template')
		contact_names = self.request.get('contact-names')
		contact_emails = self.request.get('contact-emails')
		access_code = self.request.get('access-code')
		if (access_code == "nitsuj"):
			sender = "Justin Liu <jusliu@berkeley.edu>"
		elif (access_code == "nawtihc"):
			sender = "Chitwan Kaudan <chitwank@berkeley.edu>"
		elif (access_code == "htihor"):
			sender = "Rohith Krishna <krishna.rohith@berkeley.edu"
		elif (access_code == "lanuk"):
			sender = "Kunal Desai <kunaldesai@berkeley.edu>"
		else:
			return
		params = sendEmails(email_subject, email_template, contact_names, contact_emails, sender)
		self.render_template('templates/results.html', params)

def addResponseHeaders(self):
	self.response.headers["X-Frame-Options"] = "sameorigin"
	self.response.headers["X-Content-Type-Options"] = "nosniff"
	self.response.headers["Strict-Transport-Security"] = "max-age=31536000"
	self.response.headers["Content-Type"] = "text/html; charset=utf-8"
	self.response.headers["X-XSS-Protection"] = "1; mode=block"
	self.response.headers["Cache-Control"] = "no-cache"
	self.response.headers["Set-Cookie"] = "secure; httponly;"
	self.response.headers["Pragma"] = "no-cache"
	self.response.headers["X-Permitted-Cross-Domain-Policies"] = "master-only"
	self.response.headers["Expires"] = "-1"
	return self