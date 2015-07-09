import sys
import json
import httplib2
import requests
from oauth2client.client import SignedJwtAssertionCredentials
import gdata.spreadsheets.client
import gdata.spreadsheet.service
import gdata.gauth
import datetime

#
# LOAD SETTINGS
#
settings = json.load(open('settings.json'))
oauth = json.load(open('oauth.json'))

#
# CHECK IF SCRIPT CAN RUN
#
now = datetime.datetime.now()
checkHours = now.hour in settings['run']['hours']
checkWeekend = now.weekday() >= 6

if checkWeekend:
    if not settings['run']['weekends']:
        print "This script cannot be ran at this time. Try again later."
        sys.exit(-1)

if not checkHours:
    print "This script cannot be ran at this time. Try again later."
    sys.exit(-1)

#
# CREATE CONNECTION TO GOOGLE DOCS
#
credentials = SignedJwtAssertionCredentials(
    oauth['client_email'],
    oauth['private_key'],
    scope='https://spreadsheets.google.com/feeds/',
    sub=settings['sub']
)

http = httplib2.Http()
http = credentials.authorize(http)
auth2token = gdata.gauth.OAuth2TokenFromCredentials(credentials)

clt = gdata.spreadsheets.client.SpreadsheetsClient()
clt = auth2token.authorize(clt)


#
# FOREACH LOCATIONS IN SETTINGS
#
for loc in settings['locations']:
    newRecord = {}
    newRecord['timestamp'] = str(datetime.datetime.now())
    newRecord['address'] = loc['address']

    start = 'x:' + str(settings['start']['lon']) + '+y:' + str(settings['start']['lat'])
    end = 'x:' + str(loc['lon']) + '+y:' + str(loc['lat'])

    # IF IT'S AFTER 12:00PM SWITCH DIRECTIONS (going home)
    if now.hour >= 12:
        logic = 'from=' + start + '&to=' + end
        newRecord['direction'] = 'Leaving from Location'
    else:
        logic = 'from=' + end + '&to=' + start
        newRecord['direction'] = 'Heading to Location'

    url = 'https://www.waze.com/RoutingManager/routingRequest?' + logic + '&at=0&returnJSON=true&nPaths=2&options=AVOID_TRAILS'

    req = requests.get(url)
    res = req.json()

    for route in res['alternatives']:
        newRecord['route'] = route['response']['routeName']
        routeTime = 0
        for direction in route['response']['results']:
            routeTime += direction['crossTime']
        newRecord['minutes'] = unicode(round((routeTime/60) * 1.10))  # add 10% for extra padding

        entry = gdata.spreadsheets.data.ListEntry()
        entry.from_dict(newRecord)

        clt.add_list_entry(entry, settings['spreadsheet_key'], 'od6')
