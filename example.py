#!/usr/bin/python
# A simple example showing how to use the googleweather class.

from googleweather import *

# Set the location using a post code. Setting "lang=en-gb" will return
# temperatures in Imperial units. Cache the downloaded data for 60 mins before
# reloading the data from Google and download the Google weather icons
# to the current working directory.
myForecast = googleWeather(location="LL55 4EU", lang="en-gb", expires=60, get_icons=True)

myForecast.setImageLocation("./")
myForecast.filename = "Caernarfon.xml"
forecast = myForecast.getForecast()


print "City: %s Post code: %s" % (forecast['city'][0], forecast['location'])
for i, day in enumerate(forecast['days']):
    print "%s: High: %s Low: %s Conditions: %s" % (day, forecast['high'][i], forecast['low'][i], forecast['conditions'][i])

