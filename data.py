#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
data.json is the Google Location History downloaded from

    https://www.google.com/settings/takeout/custom/location_history

Given a time, the nearest datetime point is returned. So you can seen your
position at the datetime, more or less.


Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import json
import datetime


JSON_DATA = 'data.json'


class Locations(object):
    def __init__(self, data=JSON_DATA):
        with open(data) as fp:
            res = json.load(fp)[u'locations']
            self.data = [{'ts': datetime.datetime.fromtimestamp(int(e[u'timestampMs']) / 1000.0), 'x': e[u'latitudeE7'] / 10000000.0, 'y': e[u'longitudeE7'] / 10000000.0} for e in res]

    def _find(self, d, data):
        if len(data) == 1:
            return data[0]
        if len(data) == 2:
            t1 = abs((d - data[0]['ts']).total_seconds())
            t2 = abs((d - data[1]['ts']).total_seconds())
            return data[0] if (t1 <= t2) else data[1]
        middleIndex = len(data) / 2
        middleDate = data[middleIndex]['ts']
        if (middleDate - d).total_seconds() >= 0:
            return self._find(d, data[middleIndex:])
        else:
            return self._find(d, data[:middleIndex + 1])

    def find(self, d):
        return self._find(d, self.data)


if __name__ == '__main__':
    print 'Loading locations...'
    locations = Locations()
    print 'Loaded %d locations' % len(locations.data)
    print '-' * 10
    d = datetime.datetime(2014, 2, 23, 14, 3, 13)
    print 'Searching for ', d
    print locations.find(d)