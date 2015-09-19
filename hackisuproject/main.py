#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Useless comment
import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import logging
import json
import urllib
from operator import eq
from collections import OrderedDict

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Place(ndb.Model):
    category = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

#consumer key = xcBFVugoUDNSh-YdI69i7A

class ResultsHandler(webapp2.RequestHandler):
    def post(self):
<<<<<<< HEAD
        template = jinja_environment.get_template('templates/index.html')
        example_source = urlfetch('http://api.yelp.com/v2/search?term=food&location=San+Francisco')
        logging.info(example_source)
        search_url = ('http://api.yelp.com/v2/search?term=' + '&location=San+Francisco')

        search_term = self.request.get("search")
        search_term = search_term.replace(" ", "+")


        query_url = search_url % search_term
        url_fetch_response = urlfetch.fetch(query_url)

        json_content = url_fetch_response.content
        parsed_giphy_dictionary = json.loads(json_content)




        self.response.write(template.render())

=======
        result_template = jinja_environment.get_template('templates/results.html')
        # template = jinja_environment.get_template('templates/results.html')
        # example_source = urlfetch('http://api.yelp.com/v2/search?term=food&location=San+Francisco')
        # logging.info(example_source)
        # base_url_category = ('http://api.yelp.com/v2/search?term=')
>>>>>>> 374dcdf0fe8ed599c728238c4f44a4a2e780d018

        # template_names = {}
        # template_categories = {}
        # template_locations = {}
        # search_results = []
        user_search = self.request.get('search')
        # user_term.replace(" ", "+")
        term = {'term' : user_search}
        user_term = urllib.urlencode(term)
        base_url = 'http://api.yelp.com/v2/search?term='
        search_url = base_url + user_term
        url_content = urlfetch.fetch(search_url).content
        parsed_url_dictionary = json.loads(url_content)
        yelp_url = parsed_url_dictionary
        template_vars = {"yelp1": yelp_url}
        # url_content = urlfetch.fetch(search_url).content
        # parsed_url_dictionary = json.loads(url_content)
        # template = jinja_environment.get_template('templates/results.html')
        # self.response.write(template.render())
        self.response.write(result_template.render(template_vars))

    def post(self):
        self.response.write(template.render())
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler)
], debug=True)
