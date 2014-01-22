FlickrGeoTagger
===============

Allows you to geotag your Flickr photos using a gpx file recorded by third applications/GPS devices.


Usage
-----


1. Install the project in development mode::
  
    python setup.py develop
    
2. Set your ``SECRET_KEY`` in the environment variable::

    export SECRET_KEY=''

3. Prepare the database::

    python manage.py syncdb
    
    
``flickrgeotagger`` is a shortcut for running ``python manage.py`` so you can use it to execute all management commands
    
4. Configure your flickr app credentials in the environment variables::

    export FLICKR_APP_ID=''
    export FLICKR_API_SECRET=''

Dropbox integration (optional)
++++++++++++++++++++++++++++++

Add your `Drop-in <https://www.dropbox.com/developers/dropins/chooser/js>`_ app key to the environment variable::

    export DROPBOX_APP_KEY=''
