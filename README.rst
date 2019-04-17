Introduction
============

.. image:: https://www.wildcardcorp.com/logo.png
   :height: 50
   :width: 382
   :alt: Original work by wildcardcorp.com
   :align: right

This package provides Audio and Video Dexterity content types and behaviors,
conversions and players/views.

It integrates the HTML5 media player `mediaelementjs`_ and uses
`plone.app.async`_ if installed to convert videos to common formats.

.. _mediaelementjs: http://mediaelementjs.com
.. _plone.app.async: https://pypi.python.org/pypi/plone.app.async

Features
--------

- Audio and Video types
- Integration with `mediaelementjs`_ designed for maximum forward and
  backwards compatibility
- Automatically convert video types to HTML5 compatible video formats
- Be able to add video from TinyMCE by adding a link to the audio or video
  objects and then adding one of the available Audio and Video TinyMCE styles.
- Integration with `plone.app.async`_ for conversions if installed
- Plone 4.3 syndication support
- Transcript data
- Youtube URL  (in case you want the video streamed from Youtube)
- Streaming support
- Still screen shot
- Subtitle (captioning) file in SRT format

Installation
------------

In order for video conversion to work correctly, you'll need ``ffmpeg``
installed which provides the ``avconv`` collection of command line utilities.

On Ubuntu, you should be able to install with::

    sudo apt-get install libav-tools

Plone 4
~~~~~~~

Must have plone.app.jquery >= 1.8.3


Conversion
----------

Force Conversion
~~~~~~~~~~~~~~~~

Uploaded videos can be forced through the video conversion process by enabling
the ``Force video conversion`` option. This option is useful if you would like
to transcode all videos down to a certain resolution; or if you want to enforce
a certain quality setting or video profile across all uploads.

Conversion Parameters
~~~~~~~~~~~~~~~~~~~~~

You may like to pass certain parameters to ``avconv`` to customise the video
transcoding process. Extra ``infile`` and ``outfile`` options can be configured
in the control panel per video format:

    avconv [infile options] -i infile [outfile options] outfile.{format}

The latest version of ``avconv`` on Ubuntu may require
``-strict experimental`` as an ``outfile`` option for the mp4 format.


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
``google_oauth_id`` and ``google_oauth_secret`` properties in the
Configuration Registry.

Finally, go to the url: http://plonesite/authorize-google


Development
-----------

Compiling JS
~~~~~~~~~~~~

cd wildcard/media/browser/static
make bootstrap
make prod


Support
-------

Tested on Plone 4.3.x, 5.0, 5.1 and 5.2
