# GoogleMaps version 1.02
# REFERENCE: http://py-googlemaps.sourceforge.net/
# NOTE: There is no need to obtain Google api key, just use no argument (ex. GoogleMaps() )
# This api makes extensive use of nested Python dictionary data structures to store map data elements (me no like!)
# To get miles or minutes, use 'html' as the dictionary key.  Why did Google choose 'html'?!
# Alternative: Check out geopy at http://code.google.com/p/geopy/wiki/GettingStarted
#              It provides same functionality, except no directions, and no quirky/unPythonic dictionary mappings,
#              which is much easier to understand/read than GoogleMaps dictionary-based mapping
# GoogleMaps version 2 or 3: There isn't a Python interface for version 2/3.  Have to use Javascript or URL requests.

from googlemaps import GoogleMaps

address = '24000 Honda Parkway, Marysville, OH'

print 'Geocoding = latitude, longitude of address or location'
print 'Geocoding of address:', address, ' to (latitude, longitude)'
print GoogleMaps().address_to_latlng(address), '\n'

print 'Reverse geocoding (40.278754, -83.508379):'
print GoogleMaps().latlng_to_address(40.278754, -83.508379), '\n'

destination = '3900 Morse Rd, Columbus, OH'

directions = GoogleMaps().directions(address, destination)

print 'Miles to destination: ', destination, 'from', address
# print str( directions['Directions']['Distance']['meters'] * 0.000621371192 ), 'miles\n'
# Found out 'html' is the key to use to get miles, conversion is not needed
print str( directions['Directions']['Distance']['html'] ).replace('&nbsp;mi',' miles'), '\n'

# print 'Travel duration (via car):', str( directions['Directions']['Duration']['seconds']/60 ), 'minutes', '\n'
# Found out 'html' is the key to use to get duration in minutes, conversion is not needed
print 'Travel duration (via car):', str( directions['Directions']['Duration']['html'] )

route = directions['Directions']['Routes'][0]

print 'Step-by-Step directions (in HTML):'
for step in route['Steps']:
    print step['descriptionHtml']
    print 'For', str( step['Distance']['html'] )
    print '\n'

print "Local search example: 'sushi dublin, oh'"
print 'Printing just 1st search result:'
local = GoogleMaps().local_search('sushi dublin, oh')
result = local['responseData']['results'][0]  # Get 1st search result or use loop to get first x results
print 'Title:', result['titleNoFormatting']
print 'Address:', result['streetAddress']
print 'Phone number:', result['phoneNumbers'][0]['number']
