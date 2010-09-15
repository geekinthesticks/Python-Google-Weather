#!/usr/bin/python

import urllib, os, sys
from xml.dom import minidom
import time


class googleWeather:
    def __init__(self, location="Wilkesley", postcode="SY13 4BB", lang="en-gb", expires=60, get_icons=True):
        """

        """
        self.location = location
        self.postcode = postcode
        self.lang = lang
        self.forecast = {}
        self.expires = expires
        self.imagedir = "./"
        self.base_url = "http://www.google.co.uk/ig/api?weather="
        self.google_images_url = 'http://www.google.co.uk'
        self.get_icons = get_icons

    def setBaseUrl(self, baseurl):
        """
        The url for calling the Google weather api.
        """
        self.base_url = baseurl

    def setGoogleImagesUrl(self, google_images_url):
        """
        The url where Google stores the images representing
        different weather conditions.
        """

        self.google_images_url = google_images_url

    def setLocation(self, location):
        """
        The location string is purely descriptive and is not required
        to get forecasts.
        """

        self.location = location

    def setGetIcons(self, get_icons):
        """
        You may want to use your own icons, rather than Google's.
        If you don't want to downoad the Google icons, set this to False.
        """
        self.get_icons = get_icons

    def setImageDir(self, imagedir):
        """
        Sets the directory where images are downloaded.
        """

        self.imagedir = imagedir

    def setCacheExpireTime(self, expires):
        """
        Set the time in minutes that downloaded forecasts are cached.
        """
        self.expires = expires
    

    def setPostCode(self, postcode):
        """
        The post code/zip code of the location for which you
        want to retrieve the weather.
        """
        self.postcode = postcode

    def setLang(self, lang):
        """
        Undocumented function which sets the language of the forecast.
        This may also change whether the forecast returns measurements
        in SI units or imperial units.

        Examples are "en-gb", "es"
        """
        self.lang = lang

    def setImageLocation(self, directory):
        """
        Sets the directory where downloaded images are stored.
        If you want to use your own images, set this to the directory
        cotaining your own images.
        """
        self.imagedir = directory

    def fahrenheit_to_centigrade(self, temp):
        """
        Utility function to convert temperaatures in fahrenheit to
        Celsius.

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
            if not os.path.exists(self.imagedir + '%s' % file):
                urllib.urlretrieve('%s%s' % (self.google_images_url, icon), \
                              '%s%s' % (self.imagedir, file))


    def parse_forecast_data(self, dom):
        """
        Parse the downloaded xml file to get the forecast data.
        The data is returned as a nested set of lists.
        """
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
                low.append(low_temp.getAttribute('data'))

            for high_temp in forecast_high:
                high.append(high_temp.getAttribute('data'))

            for condition in forecast_condition:
                conditions.append(condition.getAttribute('data'))

            for dayIcon in forecast_icons:
                icons.append(dayIcon.getAttribute('data'))

        if self.get_icons:
            self.download_icons(icons)

        self.forecast['days'] = days
        self.forecast['high'] = high
        self.forecast['low'] = low
        self.forecast['conditions'] = conditions
        self.forecast['icons'] = icons

        return self.forecast

    def getForecast(self):
        """
        Download the page corresponding to the location specified
        and call the function to parse the xml.

        Downloads are cached to avoid repeated queries to Google's
        server. See setCacheExpireTime. The default is 60 mins.
        """
        location_xml = self.location + ".xml"

        # Check the local xml file.

       # We need to url encode the query params.
        params = {'postcode' : self.postcode,
                  'hl' : self.lang}
        url = self.base_url + urllib.urlencode(params)

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

