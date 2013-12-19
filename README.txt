Introduction
============

This package provides Audio and Video Dexterity content types and behaviors.

It integrates the HTML5 media player mediaelementjs.


Features
--------

- Audio and Video types
- Integration with mediaelementjs
- Automatically convert video types to HTML5 compatible video formats
- Be able to add video from TinyMCE by adding a link to the audio or video
  objects and then adding one of the available Audio and Video TinyMCE styles.
- Integration with plone.app.async for conversions if installed
- Plone 4.3 syndication support


Installation
------------

In order for video conversion to work correctly, you'll need ffmpeg installed
which provides the `avconv` collection of command line utilities.

On Ubuntu, you should be able to install with::

    sudo apt-get install ffmpeg


Support
-------

Only tested on Plone 4.3
