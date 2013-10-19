FlickrGeoTagger
===============

Allows you to geotag your Flickr photos using a gpx file recorded by third applications/GPS devices.


Usage
-----


1. Install dependencies::
  

    make install


2. Prepare the database::

    python manage.py syncdb
    
3. Configure your flickr credentials in the ``settings.py`` file::

    FLICKR_APP_ID = ''
    FLICKR_API_SECRET = ''
