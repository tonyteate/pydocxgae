
import webapp2
import json
import re
import string
import random
from uuid import uuid4
import os
import jinja2
import logging
from datetime import datetime
import cgi
import base64

from urllib import unquote, urlencode
from urlparse import urlparse, parse_qs, urljoin

from google.appengine.ext.db import Blob
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

from sensitive import GITHUB_AUTH

import pydocx
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from xml.sax.saxutils import escape, unescape    

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
							   autoescape=False,
							   trim_blocks=True)

class Image(ndb.Model):

    eid = ndb.IntegerProperty(required=True)
    image = ndb.BlobProperty(required=True)
    extension = ndb.StringProperty(required=True)

    created = ndb.DateTimeProperty(auto_now_add = True, required = True)
    lastmodified = ndb.DateTimeProperty(auto_now = True)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):

        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):

        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):

        self.write(self.render_str(template, **kw))    


class ImageHandler(webapp2.RequestHandler):

    def get(self, eid):

        if not eid:
            self.response.out.write("")
            return

        eid = int(eid)

        image = Image.query(Image.eid == eid).get()

        if image:
        	self.response.headers['Content-Type'] = str("image/%s" %(image.extension or 'png'))
        	self.response.out.write(base64.b64decode(image.image))
        else:    
        	self.response.out.write("")


class MainPage(Handler):

	def render_front(self, render="", html="", malert="", pti='',ls='',pi='', gfmp=True):
		self.render("main.html", render=render, html=html, malert=malert, 
			pseudo_tab_indent=pti,list_spacing=ls,process_images=pi, gfm_preview=gfmp)

	def get(self):

		logging.error(self.request.host_url)
		self.render_front()

	def post(self):
		filedata = self.request.get('filedata')

		escape_text=True
		pseudo_tab_indent=bool(self.request.get('pseudo_tab_indent'))
		list_spacing=bool(self.request.get('list_spacing'))
		process_images=bool(self.request.get('process_images'))		
		gfm_preview = bool(self.request.get('gfm_preview'))

		logging.error(pseudo_tab_indent)
		logging.error(list_spacing)
		logging.error(process_images)

		if filedata and len(filedata) < 1e6:

			in_memory = StringIO.StringIO(filedata)

			html = ''

			parser = pydocx.Docx2Markdown(in_memory,
										  escape_text=escape_text,
										  pseudo_tab_indent=pseudo_tab_indent,
										  list_spacing=list_spacing,
										  process_images=process_images)
			render = parser.parsed

			if process_images:
				images = parser.images

				if images:
					logging.error(len(images))
					image_models = []
					for eid, info in images.iteritems():
						image_model = Image(extension=info[0], image=Blob(info[1]), eid=eid)
						image_models.append(image_model)
					ndb.put_multi(image_models)

			if gfm_preview:
				result = urlfetch.fetch(url='https://api.github.com/markdown', 
										payload=json.dumps({'text': render}), 
										method=urlfetch.POST,
										headers={'User-Agent': 'Mozilla/5.0',
												 'Authorization': 'Basic %s' 
												 %base64.b64encode(GITHUB_AUTH)})

				logging.error(result.status_code)
				logging.error(result.headers)
				logging.error(result.content)
				if result.status_code == 200:
					html = result.content.decode("utf8")

			self.render_front(render, html, pti=pseudo_tab_indent,ls=list_spacing,pi=process_images,gfmp=gfm_preview)


		else:
			self.render_front(malert="You didn't choose a file...", pti=pseudo_tab_indent,ls=list_spacing,pi=process_images, gfmp=gfm_preview)


class WelcomeHandler(Handler):

    def get(self): 

        self.response.out.write('<form method="post"><input type="submit" value="Go!"/>')


    def post(self):

        url = self.request.get("url")
        self.response.out.write(url)
 


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/img/([0-9]+)/?', ImageHandler),                                             
                               ], debug=True)
