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

Video Adapter - Support for various external services
-----------------------------------------------------

With the help of adapters it's now possible to embed videos
from different sources other than YouTube.

By default only YouTube adapter is registered. If you need to provide a new provider, just register an adapter like this::

  <adapter
      factory = ".foo_adapter.FooVideoEmbedCode"
      name = "foo.com" />

And the code should be something like this::
  from wildcard.video.adapters.video_embed_code import BaseEmbedCode
  from wildcard.media.interfaces import IVideoEmbedCode
  from wildcard.media.interfaces import IVideoEnabled
  from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
  from zope.interface import implementer
  from zope.interface import Interface
  from zope.component import adapter


  @implementer(IVideoEmbedCode)
  @adapter(IVideoEnabled, Interface)
  class FooVideoEmbedCode(BaseEmbedCode):
      template = ViewPageTemplateFile("foo_template.pt")

The template file is the html snippet used for embedding the video.
The name of the adapter is the domain name of the streaming service.

If you set a video_url like "https://foo.com/videos/123456", the adapter with name "foo.com" will be used.
If the service uses more domains (for example youtube.com or youtu.be), you need to register several adapters for each domain.

If you link a direct link to an mp4 file, a default adapter will be used.


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
