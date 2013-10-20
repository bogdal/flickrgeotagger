FlickrGeoTagger
===============

Allows you to geotag your Flickr photos using a gpx file recorded by third applications/GPS devices.


Usage
-----


1. Install dependencies::
  

    make install

2. Prepare the database::

    python manage.py syncdb
    
3. Configure your flickr app credentials in the ``settings.py`` file::

    FLICKR_APP_ID = ''
    FLICKR_API_SECRET = ''

Dropbox integration (optional)
++++++++++++++++++++++++++++++

Add your `Drop-in <https://www.dropbox.com/developers/dropins/chooser/js>`_ app key to the ``settings.py`` file::

  DROPBOX_APP_KEY = ''
