#!/usr/bin/python

import urllib, os, sys
from xml.dom import minidom
import ConfigParser
import time

#IMAGES_PATH = '/var/www/vhosts/ian-barton/images/'
IMAGES_PATH = '/home/ian/devel/python_google_weather/images/'
GOOGLE_IMAGES_URL = 'http://www.google.co.uk'
#WEATHER_XML = '~/devel/python_google_weather/google_weather.xml'
OUT_FILE = "/var/www"
BASE_URL = "http://www.google.co.uk/ig/api?weather="

def fahrenheit_to_centigrade(temp):
    """
    Celsius = (Temp_in_Fahrenheit - 32) / (9.0/5.0)
    """
    celsius = int(temp)
    celsius = (celsius -32)/ (9.0/5.0)

    return "%.1f" % (celsius)

def read_config_locations():
    """
    Read the configuration data.
    Locations are specified as Name = Post code
    """
    location_data = {}

    config = ConfigParser.RawConfigParser()

    config.read(".googleweather")
    if config == None:
        print "Unable to read configuration file: ", CONFIG_FILE
        sys.exit(2)

    cities = config.items("locations")
    locations = {}

    for city in cities:
        locations[city[0]] = city[1]

    return locations

def read_config_settings():
    """
    Read the configuration data.

    """

    config = ConfigParser.RawConfigParser()

    config.read(".googleweather")
    if config == None:
        print "Unable to read configuration file: ", CONFIG_FILE
        sys.exit(2)

    config_settings = config.items("settings")
    print config_settings

    settings = {}

    for setting in config_settings:
        settings[setting[0]] = setting[1]

    if not('images' in settings):
         print "Image directory not set in .googleweather."
         sys.exit(2)

    if not('html' in settings):
         print "Html output file set in .googleweather."
         sys.exit(2)

    return settings



# Images.
# http://www.google.co.uk/ig/images/weather/sunny.gif

def download_icons(icon_list):
    """
    Download weather icons if they are not
    already cached locally.
    """
    for icon in icon_list:
        (dir, file) = os.path.split(icon)
        if not os.path.exists(IMAGES_PATH + '%s' % file):
            urllib.urlretrieve('%s%s' % (GOOGLE_IMAGES_URL, icon), \
                          '%s%s' % (IMAGES_PATH, file))


def parse_forecast_data(dom):
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

def get_weather(location, postcode):
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

def create_html(locations, settings):
    """
    Create an html file from the weather data.
    """


    forecast_data_list = []
    fout = open(settings['html'], "w")
    for location in locations:
        forecast_data_list.append(get_weather(location, locations[location]))

    # Create html file.
    for city in forecast_data_list:
        fout.write('<table border="1">')
        fout.write('<tr>')
        fout.write( '<h3>%s</h3>\n' % (city['location']))
        for i in range(len(city['days'])):
            # icons
            (path, icon) = os.path.split(city['icons'][i])
            fout.write('<td>')
            fout.write( '<img src="%s/%s" <alt="%s"><br/>' % (settings['images'], icon, icon) )

            fout.write( "%s<br/> <ul> <li>High: %s</li> <li>Low: %s</li> <li>Conditions: %s</li> </ul>\n" % (city['days'][i], city['high'][i], city['low'][i], city['conditions'][i]) )
            fout.write('</td>')

    fout.write('</tr>')
    fout.write('</table>\n')


    fout.close()

def main():

    locations = read_config_locations()
    settings = read_config_settings()

    forecast_data_list = []
    print "Locations: ", locations
    for location in locations:
        forecast_data_list.append(get_weather(location, locations[location]))


    create_html(locations, settings)
    print settings
    #for setting in settings:
    #    print setting
    #print forecast_data

if __name__ == '__main__':
    main()

