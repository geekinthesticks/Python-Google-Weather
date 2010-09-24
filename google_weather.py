#!/usr/bin/python

import os, sys
from googleweather import *
import ConfigParser
import time

ICON_LIB = "/usr/share/icons/gnome/32x32/status"

weather_icons = {"Chance of Rain" : "weather-showers-scattered.png",
    "Chance of Snow" : "weather-snow.png",
    "Chance of Storm" : "weather-storm.png",
    "Cloudy" : "weather-overcast.png",
    "Dust" : "weather-fog.png",
    "Flurries" : "weather-storm.png",
    "Fog" : "weather-fog.png",
    "Haze" : "weather-fog.png",
    "Icy" : "weather-snow.png",
    "Mist" : "weather-storm.png",
    "Mostly Cloudy" : "weather-overcast.png",
    "Mostly Sunny" : "weather-clear.png",
    "Partly Cloudy" : "weather-few-clouds.png",
    "Rain" : "weather-showers.png",
    "Sleet" : "weather-snow.png",
    "Smoke" : "weather-fog.png",
    "Snow" : "weather-snow.png",
    "Storm" : "weather-storm.png",
    "Thunderstorm" : "weather-storm.png",
    "Sunny" : "weather-clear.png",
    "Clear" : "weather-clear.png"}
 


OUT_FILE = "/var/www"
BASE_URL = "http://www.google.co.uk/ig/api?weather="


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
    print locations
    

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
    #print config_settings

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




def create_html(locations, settings):
    """
    Create an html file from the weather data.
    """


    forecast_data_list = []
    fout = open(settings['html'], "w")
    myWeather = googleWeather()
    for location in locations:
        #print "Location: ", location
        myWeather.setLocation(location)
        myWeather.setPostCode(locations[location])
        myWeather.setImageLocation('/home/ian/devel/python_google_weather/images/')
        forecast = myWeather.getForecast()
        forecast_data_list.append(forecast)

        #forecast_data_list.append(get_weather(location, locations[location]))

    # Create html file.
    for city in forecast_data_list:
        print "City: ", city
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

    myWeather = googleWeather()

    forecast_data_list = []
    forecast = []
    xoffset = 0
    yoffset = 34

    #print "Locations: ", locations
    for location in locations:
        myWeather.setLocation(location)
        myWeather.setPostCode(locations[location])
        myWeather.setImageLocation('/home/ian/devel/python_google_weather/images/')
        forecast = myWeather.getForecast()
        #forecast_data_list.append(forecast)
        print "City: ", forecast['city'][0]
        # print forecast
        
        for i, day in enumerate(forecast['days']):
            yoffset = yoffset + 34
            #print weather_icons[forecast['conditions'][i]]
            icon = ICON_LIB + "/"  + weather_icons[forecast['conditions'][i]]
            #print icon
            print "${color yellow} ${offset 36}%s: High: %s Low: %s ${image %s -p %s,%s}" % (day, forecast['high'][i], forecast['low'][i], icon, xoffset, yoffset)
        print "\n"


        #forecast_data_list.append(myWeather.getForecast(location, locations[location]))


    #create_html(locations, settings)
    #print settings
    #for setting in settings:
    #    print setting
    #print forecast_data

if __name__ == '__main__':
    main()

