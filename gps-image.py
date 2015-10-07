#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Simple script to add GPS data to photos. The GPS info are taken from your Google
location history.

First of all you need to download all you location history from Google Takeout
in JSON format.

    https://www.google.com/settings/takeout/custom/location_history

You have to save the JSON file in data.json (or somethig else, depending on
data.py).

Usage

    python gps-image.py imgdir

Every image in imgdir is checked for datetime metadata. For each datetime info,
the nearest datetime point is searched in the JSON file and the corrisponding
coords are applied to the photo.


Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import sys, os, datetime

import pexif

import data


class Img(object):

    def __init__(self, fName):
        try:
            self.img = pexif.JpegFile.fromFile(fName)
            self.fName = fName
        except pexif.JpegFile.InvalidFile:
            raise TypeError

    def getDate(self):
        try:
            primary = self.img.get_exif().get_primary()
            try:
                return datetime.datetime.strptime(primary.DateTime, '%Y:%m:%d %H:%M:%S')
            except:
                pass
            try:
                return datetime.datetime.strptime(primary.ExtendedEXIF.DateTimeDigitized,
                        '%Y:%m:%d %H:%M:%S')
            except:
                pass
            try:
                return datetime.datetime.strptime(primary.ExtendedEXIF.DateTimeOriginal,
                        '%Y:%m:%d %H:%M:%S')
            except:
                pass
            return datetime.datetime.strptime(primary.ExtendedEXIF.DateTime,
                    '%Y:%m:%d %H:%M:%S')
        except:
            raise NoDateError

    def getCoord(self):
        try:
            return self.img.get_geo()
        except:
            raise NoCoordError()

    def setCoord(self, lat, lng):
        self.img.set_geo(lat, lng)
        self.img.writeFile(self.fName)


if __name__ == '__main__':
    locations = data.Locations()

    dirName = sys.argv[1]
    for (subdir, _, files) in os.walk(dirName):
        for f in files:
            fName = os.path.join(subdir, f)
            try:
                img = Img(fName)
                print img.fName
                c = locations.find(img.getDate())
                img.setCoord(c['x'], c['y'])
            except TypeError:
                pass