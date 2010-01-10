#!/usr/bin/python

import urllib, os, sys
from time import strftime
from xml.dom import minidom

IMAGES_PATH = '/home/ian/devel/python_google_weather'
GOOGLE_IMAGES_URL = 'http://www.google.co.uk/ig'
WEATHER_XML = '~/devel/python_google_weather/google_weather.xml'

# Images.
# http://www.google.co.uk/ig/images/weather/sunny.gif

def download_icons(icon_list):
    """
    Download weather icons if they are not
    already cached locally.
    """
    for icon in icon_list:
        if not os.path.exists(IMAGES_PATH + '%s' % icon):
            print "Getting image.\n"
            urllib.urlretrieve('%s%s' % (GOOGLE_IMAGES_URL, icon), \
                          '%s%s' % (IMAGES_PATH, icon))
            #print  '%s%s' % (IMAGES_PATH, icon)


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
            low.append(low_temp.getAttribute('data'))

        for high_temp in forecast_high:
            high.append(high_temp.getAttribute('data'))

        for condition in forecast_condition:
            conditions.append(condition.getAttribute('data'))

        for dayIcon in forecast_icons:
            icons.append(dayIcon.getAttribute('data'))

    download_icons(icons)    

    print 'days: ', days
    forecast_data['days'] = days
    forecast_data['high'] = high
    forecast_data['low'] = low
    forecast_data['conditions'] = conditions
    forecast_data['icons'] = icons

    return forecast_data
        

def main():
    # Check the local xml file.
    if os.path.exists(WEATHER_XML):    
        # Check its time stamp.
        statinfo = os.path.stat(os.path.expanduser(WEATHER_XML))
        # file_time = time.localtime(statinfo.st_mtime)

        # Compare file time to current time.
        # If it's more than 4 hrs old grab a new forecast.
        if (time.localtime() > (statinfo.st_mtime + (4*3600))):
            print 'File too old.'
            # Open the url and save to a file.
            urllib.retrieve('http://www.google.co.uk/ig/api?weather=sy134bb', os.path.expanduser(WEATHER_XML))
        else:    
             dom = minidom.parse(urllib.urlopen('http://www.google.co.uk/ig/api?weather=sy134bb'))
            
    else:
        urllib.urlretrieve('http://www.google.co.uk/ig/api?weather=sy134bb', os.path.expanduser(WEATHER_XML))
        dom = minidom.parse(os.path.expanduser(WEATHER_XML))
    #dom = minidom.parse(urllib.urlopen('google_weather.xml'))        

    forecast_data = parse_forecast_data(dom)

    print "City: %s" % (forecast_data['city'][0])
    print forecast_data['days']
    for i in range(len(forecast_data['days'])):
        print "%s High: %s Low: %s Conditions: %s" % (forecast_data['days'][i], forecast_data['high'][i], forecast_data['low'][i], forecast_data['conditions'][i])

if __name__ == '__main__':
    main()
    sys.exit()
