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

def get_weather_info(query):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?&'
    api_key_url = '&units=imperial&APPID=341e54aef9ae5224b6094459078293b8'
    weather_data_source = urlfetch.fetch(base_url + query + api_key_url)
    weather_json_content = weather_data_source.content
    parsed_weather_dictionary = json.loads(weather_json_content)
    return parsed_weather_dictionary

def get_city_info(parsed_weather_dictionary):
    ## WEATHER ##
    city_name = parsed_weather_dictionary['name']
    country = parsed_weather_dictionary['sys']['country']
    weather_description = parsed_weather_dictionary['weather'][0]['description']
    temperature = parsed_weather_dictionary['main']['temp']
    min_temp = parsed_weather_dictionary['main']['temp_min']
    max_temp = parsed_weather_dictionary['main']['temp_max']
    humidity = parsed_weather_dictionary['main']['humidity']
    wind_speed = parsed_weather_dictionary['wind']['speed']


    search_term = urllib.quote_plus(city_name)
    search_term = search_term.replace('%20', '+')


    # NEARBY RESTAURANTS AND BUSINESSES ##
    parsed_yelp_list = yelp.query_api(search_term)
    logging.info(parsed_yelp_list)
    business_list = []
    business = {}
    has_yelp = True
    if len(parsed_yelp_list) != 0:
        for i in range(len(parsed_yelp_list)):
            business['name'] = urllib.unquote(parsed_yelp_list[i]['id']).replace('-', ' ').title()
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
        'description': weather_description,
        'temperature': int(temperature),
        'min_temp': int(min_temp),
        'max_temp': int(max_temp),
        'humidity': humidity,
        'wind_speed': wind_speed,
        'has_yelp': has_yelp,
        'business_list': business_list
        }

    return template_vars

# class Place(ndb.Model):
#     category = ndb.StringProperty(required = True)
#     name = ndb.StringProperty(required = True)
#     location = ndb.StringProperty(required = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

#consumer key = xcBFVugoUDNSh-YdI69i7A

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        ## DISPLAYS CITY INFORMATION ##
        query = 'q=' + self.request.get('search')
        query = query.replace(' ', '+')

        parsed_weather_dictionary = get_weather_info(query)
        if 'name' in parsed_weather_dictionary:
            template_vars = get_city_info(parsed_weather_dictionary)
            template = jinja_environment.get_template('templates/results.html')
            self.response.write(template.render(template_vars))
        else:
            template = jinja_environment.get_template('templates/error.html')
            self.response.write(template.render({'error_description': 'Invalid search. Please try again!'}))

class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/error.html')
        self.response.write(template.render())

class RandomHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/random.html')
        places_list = ['springfield', 'dallas', 'chicago', 'orlando', 'lincoln', 'iowa city', 'ames', 'seattle']
        randNum = random.randint(0,7)
        query = 'q=' + places_list[randNum]
        query = query.replace(' ', '+')
        parsed_weather_dictionary = get_weather_info(query)
        if 'name' in parsed_weather_dictionary:
            template_vars = get_city_info(parsed_weather_dictionary)
            self.response.write(template.render(template_vars))
        else:
            template = jinja_environment.get_template('templates/error.html')
            self.response.write(template.render({'error_description': 'Invalid search. Please try again!'}))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/error', ErrorHandler),
    ('/random', RandomHandler)
], debug=True)
