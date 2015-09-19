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
import oauth2
import webapp2
import json
import random
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import jinja2
import os

import random
import csv
import logging
import urllib
import yelp
from collections import OrderedDict
import urllib
from operator import eq


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def get_city_list():
    city_list = []
    f = open(os.path.join(os.path.dirname(__file__), 'csv/cities.csv'))
    csv_f = csv.reader(f)
    for row in csv_f:
      city_list.append(row[2])
    city_list = set(city_list)
    return city_list

def parse_dict(query):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?&'
    api_key_url = '&units=imperial&APPID=341e54aef9ae5224b6094459078293b8'
    data_source = urlfetch.fetch(base_url + query + api_key_url)
    json_content = data_source.content
    parsed_dictionary = json.loads(json_content)

    return parsed_dictionary

def get_city_info(parsed_dictionary):
    ## WEATHER ##
    # base_url = 'http://api.openweathermap.org/data/2.5/weather?&'
    # api_key_url = '&units=imperial&APPID=341e54aef9ae5224b6094459078293b8'
    # weather_data_source = urlfetch.fetch(base_url + query + api_key_url)
    # weather_json_content = weather_data_source.content
    # parsed_weather_dictionary = json.loads(weather_json_content)

    city_name = parsed_dictionary['name']
    country = parsed_dictionary['sys']['country']


    temperature = parsed_dictionary['main']['temp']
    min_temp = parsed_dictionary['main']['temp_min']
    max_temp = parsed_dictionary['main']['temp_max']


    icon_url = 'http://openweathermap.org/img/w/%s.png' % weather_icon

    search_term = urllib.quote_plus(city_name)
    search_term = search_term.replace('%20', '+')
    search_term = search_term.replace(' ', '+')



    # NEARBY RESTAURANTS AND BUSINESSES ##
    parsed_yelp_list = yelp.query_api(search_term)
    logging.info(parsed_yelp_list)
    business_list = []
    business = {}
    has_yelp = True
    if len(parsed_yelp_list) != 0:
        for i in range(len(parsed_yelp_list)):
            business['name'] = urllib.unquote(parsed_yelp_list[i]['id']).replace('-', ' ').title()
            logging.info(urllib.unquote(parsed_yelp_list[i]['id']))
            business['rating'] = parsed_yelp_list[i]['rating']
            business['url'] = parsed_yelp_list[i]['url']
            address = ', '.join(parsed_yelp_list[i]['location']['display_address'])
            business['address'] = urllib.unquote(address)
            business_list.append(business.copy())
    else:
        has_yelp = False



    template_vars = {
        'city_name': city_name,
        'country': country,
        'temperature': int(temperature),
        'has_yelp': has_yelp,
        'business_list': business_list}

    return template_vars


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
    def get(self):

        if self.request.get('search-type') == 'zip':
            query = 'zip=' + self.request.get('search')
        elif self.request.get('search-type') == 'latlon':
            query = 'lat=%s&lon=%s' % (self.request.get('lat'), self.request.get('lon'))
        else:
            query = 'q=' + self.request.get('search')
            query = query.replace(' ', '+')

        parsed_dictionary = get_city_info(query)
        if 'name' in parsed_dictionary:
            template_vars = get_city_info(parsed_dictionary)
            template = jinja_environment.get_template('templates/results.html')
            self.response.write(template.render(template_vars))
        else:
            template = jinja_environment.get_template('templates/error.html')
            self.response.write(template.render({'error_description': 'Invalid search. Please try again!'}))

class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/error.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/error', ErrorHandler)
], debug=True)
