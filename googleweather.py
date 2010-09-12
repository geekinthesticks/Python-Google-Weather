#!/usr/bin/python

import urllib, os, sys
from xml.dom import minidom
import time

BASE_URL = "http://www.google.co.uk/ig/api?weather="
IMAGES_PATH = '/home/ian/devel/python_google_weather/images/'
GOOGLE_IMAGES_URL = 'http://www.google.co.uk'


class googleWeather:
    def __init__(self, location="Wilkesley", postcode="SY13 4BB", lang="en-gb", expires=60):
        """

        """
        self.location = location
        self.postcode = postcode
        self.lang = lang
        self.forecast = {}
        self.expires = expires

    def setLocation(self, location):
        """
    
        """

        self.location = location

    def setPostCode(self, postcode):
        """

        """
        self.postcode = postcode

    def setLang(self, lang):
        """

        """
        self.lang = lang

    def fahrenheit_to_centigrade(self, temp):
        """
        Celsius = (Temp_in_Fahrenheit - 32) / (9.0/5.0)
        """
        celsius = int(temp)
        celsius = (celsius -32)/ (9.0/5.0)

        return "%.1f" % (celsius)

    # Images.
    # http://www.google.co.uk/ig/images/weather/sunny.gif

    def download_icons(self, icon_list):
        """
        Download weather icons if they are not
        already cached locally.
        """
        for icon in icon_list:
            (dir, file) = os.path.split(icon)
            if not os.path.exists(IMAGES_PATH + '%s' % file):
                urllib.urlretrieve('%s%s' % (GOOGLE_IMAGES_URL, icon), \
                              '%s%s' % (IMAGES_PATH, file))


    def parse_forecast_data(self, dom):
        city = []
        days = []
        low = []
        high = []
        conditions = []
        icons = []

        conditions_list = dom.getElementsByTagName('forecast_conditions')
        forecast_info = dom.getElementsByTagName('forecast_information')

        for info in forecast_info:
            city_data = info.getElementsByTagName('city')
            city.append(city_data[0].getAttribute('data'))

            self.forecast['city'] = city

        for forecast in conditions_list:
            forecast_days = forecast.getElementsByTagName('day_of_week')
            forecast_low = forecast.getElementsByTagName('low')
            forecast_high = forecast.getElementsByTagName('high')
            forecast_condition = forecast.getElementsByTagName('condition')
            forecast_icons = forecast.getElementsByTagName('icon')

            for day in forecast_days:
                days.append(day.getAttribute('data'))

            for low_temp in forecast_low:
                low.append(self.fahrenheit_to_centigrade(low_temp.getAttribute('data')))

            for high_temp in forecast_high:
                high.append(self.fahrenheit_to_centigrade(high_temp.getAttribute('data')))

            for condition in forecast_condition:
                conditions.append(condition.getAttribute('data'))

            for dayIcon in forecast_icons:
                icons.append(dayIcon.getAttribute('data'))

        self.download_icons(icons)

        self.forecast['days'] = days
        self.forecast['high'] = high
        self.forecast['low'] = low
        self.forecast['conditions'] = conditions
        self.forecast['icons'] = icons

        return self.forecast

    def getForecast(self):
        """

        """
        location_xml = self.location + ".xml"

        # Check the local xml file.

       # We need to url encode the query params.
        params = {'postcode' : self.postcode}
        url = BASE_URL + urllib.urlencode(params)

        if os.path.exists(location_xml):
            # Check its time stamp.
            statinfo = os.stat(location_xml)
            # file_time = time.localtime(statinfo.st_mtime)

            # Compare file time to current time.
            # If it's more than self.expires hours old grab a new forecast.

            if (time.mktime(time.localtime()) > (statinfo.st_mtime + (60 * self.expires))):
                print 'File too old:', location_xml
                # Open the url and save to a file.
                urllib.urlretrieve(url, location_xml)
                print "Getting: %s" % (url)

        else:
            urllib.urlretrieve(url, location_xml)
            print "Getting: %s" % (url)

        dom = minidom.parse(location_xml)
        self.forecast = self.parse_forecast_data(dom)
        self.forecast['location'] = self.location

        return self.forecast

