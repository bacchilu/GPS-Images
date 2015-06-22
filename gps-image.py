#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Simple script to add GPS data to photos. The GPS info are taken from your Google
location history, on https://maps.google.com/locationhistory.

Usage

First you have to run this:

    python gps-image.py imgdir

Every image in imgdir is checked for datetime metadata. When finisched you are
suggested to download a particular .kml file from you google location history.
For example you are suggested to download something like

    https://maps.google.com/locationhistory/b/0/kml?startTime=1407854686000&endTime=1408294947000

the parameters are evaluated according with you photos datetime metadata.

Finally you have to run this:

    python gms-image.py imgdir file.kml

To create gps tagged data in every image. Of course the best fit is searched,
according to the date and time of the photo and where you resulting to be
according to the kml file.


Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import datetime
import sys
import os
import pexif

SCRIPT_NAME = sys.argv[0]


class KmlContent(object):

    def __init__(self, fname):
        self.content = []
        self.parse(fname)

    def parse(self, fname):
        '''
        Extract datetimes and coordinates from the file
        '''

        with open(fname) as fp:
            for l in fp:
                if l.startswith('<when>'):
                    d = datetime.datetime.strptime(l[6:-14],
                            '%Y-%m-%dT%H:%M:%S.%f')
                    c = fp.next()[10:-12].split()[:-1]
                    c = [float(c[1]), float(c[0])]
                    self.content.append((d, c))

    def getCoord(self, dt):
        '''
        Given a datetime, returns the nearest coord
        '''

        lastDelta = None
        lastCoord = None
        for (d, c) in self.content:
            delta = abs((dt - d).total_seconds())
            if lastDelta is None or delta < lastDelta:
                lastDelta = delta
                lastCoord = c
        return tuple(lastCoord)


class NoDateError(Exception):

    pass


class NoCoordError(Exception):

    pass


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


def fileIterator(dirName):
    '''
    Iterate images
    '''

    for (subdir, _, files) in os.walk(dirName):
        for f in files:
            yield os.path.join(subdir, f)


def fase1(dirName):
    '''
    Iterate al files in dirName checking for images with datetimes in EXIF
    metadata
    '''

    dates = []
    for f in fileIterator(dirName):
        try:
            im = Img(f)
            d = im.getDate()
            dates.append(d)
            print '"%s" has date [%s]' % (im.fName, d)
        except TypeError:
            print '"%s" is not an image I can manage. [skip]' % f
        except NoDateError:
            print '"%s" does not not contain datetime info. [skip]' % f

    print
    print 'Ok. I found dates from "%s" to "%s"' % (min(dates),
            max(dates))

    startEpoch = int((min(dates)
                     - datetime.timedelta(days=1)).strftime('%s')) \
        * 1000
    endEpoch = int((max(dates)
                   + datetime.timedelta(days=1)).strftime('%s')) * 1000
    print 'Try downloading this:'
    print '\thttps://maps.google.com/locationhistory/b/0/kml?startTime=%d&endTime=%d' \
        % (startEpoch, endEpoch)
    print 'And execute again:'
    print '\tpython %s %s file.kml' % (SCRIPT_NAME, dirName)


def fase2(dirName, kml):
    '''
    Iterates al files in dirName setting coords, according to datetime and the
    content of the kml file
    '''

    kmlContent = KmlContent(kml)
    for f in fileIterator(dirName):
        try:
            im = Img(f)
            d = im.getDate()
            try:
                coord = im.getCoord()
                print '"%s" had old coordinates. [skip]' % f
            except NoCoordError:
                newCoord = kmlContent.getCoord(d)
                im.setCoord(newCoord[0], newCoord[1])
                print f, 'has new coordinates at', coord
        except TypeError:
            print '"%s" is not an image I can manage. [skip]' % f
        except NoDateError:
            print '"%s" does not not contain datetime info. [skip]' % f


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        fase1(sys.argv[1])

    if len(sys.argv) == 3:
        fase2(sys.argv[1], sys.argv[2])
