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
        self.response.write(template.render({
            'search': search,
            'search1': search1
        }))


    def post(self):



        search_term = self.request.get("search")
        search_term = search_term.replace(" ", "+")


        search_term1 = self.request.get("search")
        search_term1 = search_term.replace(" ", "+")

        data_source = urlfetch('http://api.yelp.com/v2/search?term=food&location=San+Francisco')
        data_source = urlfetch('http://api.yelp.com/v2/search?term=
                                                search_term
                                                "&location'=San+Francisco
                                                )



class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        # template_names = {}
        # template_categories = {}
        # template_locaitons = {}
        # user_search = self.request.get('search')
        # template = jinja_environment.get_template('templates/search.html')
        # term = {'term' : user_search}
        # search_term = urllib.urlencode(term)
        # base_url = 'http://api.yelp.com/v2/search?term='
        # search_url = base_url + search_term
        # url_content = urlfetch.fetch(search_url).content
        # parsed_url_dictionary = json.loads(url_content)
        # template = jinja_environment.get_template('templates/results.html')
        # self.response.write(template.render())
        template = jinja_environment.get_template('templates/result.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler)
], debug=True)
