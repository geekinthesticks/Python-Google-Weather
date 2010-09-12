#!/usr/bin/python

import urllib, os, sys
from xml.dom import minidom
import time

class googleWeather:
    def __init__(self, location="Wilkesley", postcode="SY13 4BB", lang="en-gb"):
        """

        """
        self.location = location
        self.postCode = postcode
        self.lang = lang


    def setLocation(self, location):
    """
    
    """

        self.location = location

    def setPostCode(self, PostCode):
    """

    """
        self.postCode = postCode

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
        forecast_data = {}
        conditions_list = dom.getElementsByTagName('forecast_conditions')
        forecast_info = dom.getElementsByTagName('forecast_information')

        for info in forecast_info:
            city_data = info.getElementsByTagName('city')
            city.append(city_data[0].getAttribute('data'))

            forecast_data['city'] = city

        for forecast in conditions_list:
            forecast_days = forecast.getElementsByTagName('day_of_week')
            forecast_low = forecast.getElementsByTagName('low')
            forecast_high = forecast.getElementsByTagName('high')
            forecast_condition = forecast.getElementsByTagName('condition')
            forecast_icons = forecast.getElementsByTagName('icon')

            for day in forecast_days:
                days.append(day.getAttribute('data'))

            for low_temp in forecast_low:
                low.append(fahrenheit_to_centigrade(low_temp.getAttribute('data')))

            for high_temp in forecast_high:
                high.append(fahrenheit_to_centigrade(high_temp.getAttribute('data')))

            for condition in forecast_condition:
                conditions.append(condition.getAttribute('data'))

            for dayIcon in forecast_icons:
                icons.append(dayIcon.getAttribute('data'))

        download_icons(icons)

        forecast_data['days'] = days
        forecast_data['high'] = high
        forecast_data['low'] = low
        forecast_data['conditions'] = conditions
        forecast_data['icons'] = icons

        return forecast_data

    def getForecast(self, location, postcode):
        """

        """
        location_xml = location + ".xml"

        # Check the local xml file.

       # We need to url encode the query params.
        params = {'postcode' : postcode}
        url = BASE_URL + urllib.urlencode(params)

        if os.path.exists(location_xml):
            # Check its time stamp.
            statinfo = os.stat(location_xml)
            # file_time = time.localtime(statinfo.st_mtime)

            # Compare file time to current time.
            # If it's more than 4 hrs old grab a new forecast.

            if (time.mktime(time.localtime()) > (statinfo.st_mtime + (4*3600))):
                print 'File too old:', location_xml
                # Open the url and save to a file.
                urllib.urlretrieve(url, location_xml)
                print "Getting: %s" % (url)

        else:
            urllib.urlretrieve(url, location_xml)
            print "Getting: %s" % (url)

        dom = minidom.parse(location_xml)
        forecast_data = parse_forecast_data(dom)
        forecast_data['location'] = location

        return forecast_data
