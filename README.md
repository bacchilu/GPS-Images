# GPS-Images
Python script to populate GPS data in a directory of images, using [Google Location History data](https://maps.google.com/locationhistory).

# Usage

First of all you need to download all you location history from Google Takeout
in JSON format.

    https://www.google.com/settings/takeout/custom/location_history

You have to save the JSON file in _data.json_ (or somethig else, depending on _data.py_).

Then you can run:

    python gps-image.py imgdir

Every image in imgdir is checked for datetime metadata. For each datetime info, the nearest datetime point is searched in the JSON file and the corrisponding coords are applied to the photo.