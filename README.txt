Introduction
============

.. image:: https://www.wildcardcorp.com/logo.png
   :height: 50
   :width: 382
   :alt: Original work by wildcardcorp.com
   :align: right
   
This package provides Audio and Video Dexterity content types and behaviors, conversions and players/views.

It integrates the HTML5 media player mediaelementjs and uses Async if installed to convert videos to common formats.


Features
--------

- Audio and Video types
- Integration with mediaelementjs designed for maximum forward and backwards compatibility
- Automatically convert video types to HTML5 compatible video formats
- Be able to add video from TinyMCE by adding a link to the audio or video
  objects and then adding one of the available Audio and Video TinyMCE styles.
- Integration with plone.app.async for conversions if installed
- Plone 4.3 syndication support
- Transcript data
- Youtube URL  (in case you want the video streamed from Youtube)
- Streaming support
- Still screen shot
- Subtitle (captioning) file in SRT format

Installation
------------

In order for video conversion to work correctly, you'll need ffmpeg installed
which provides the `avconv` collection of command line utilities.

On Ubuntu, you should be able to install with::

    sudo apt-get install libav-tools


YouTube API Support
-------------------

Since version 2.0, YouTube integration is supported.
Videos can automatically be uploaded to a configured YouTube account.

Install
~~~~~~~

Different install requirements::

    eggs = 
        ...
        wildcard.media[youtube]
        ...

Then, setup a google api with oauth access and configure the 
google_oauth_id and google_oauth_secret properties in the Configuration Registry.

Finally, go to the url: http://plonesite/authorize-google


Support
-------

Only tested on Plone 5.0, 4.3.x, Plone 4.1

