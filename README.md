# GPS-Images
Python script to populate GPS data in a directory of images, using [Google Location History data](https://maps.google.com/locationhistory).

# Usage

First you have to run this:

    python gps-image.py imgdir

Every image in imgdir is checked for datetime metadata. When finisched you are suggested to download a particular .kml file from you google location history.

For example you are suggested to download something like

    https://maps.google.com/locationhistory/b/0/kml?startTime=1407854686000&endTime=1408294947000

the parameters are evaluated according with you photos datetime metadata.

Finally you have to run this:

    python gms-image.py imgdir file.kml

To create gps tagged data in every image. Of course the best fit is searched, according to the date and time of the photo and where you resulting to be according to the kml file.