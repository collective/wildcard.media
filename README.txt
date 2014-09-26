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


Support
-------

Only tested on Plone 4.3.x, Plone 4.1
