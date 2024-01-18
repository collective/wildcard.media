/* global require */

if (window.jQuery) {
  define("jquery", function () {
    return window.jQuery;
  });
}

require(["jquery", "wildcard-patterns-video"], function ($) {
  "use strict";

  $(document).ready(function () {
    $("span.wcvideo a").each(function () {
      var $a = $(this);
      var $span = $a.parents("span.wcvideo");
      var width, height;
      if ($span.hasClass("video-large")) {
        width = 720;
        height = 480;
      } else if ($span.hasClass("video-small")) {
        width = 320;
        height = 240;
      }
      $.ajax({
        url: $a.attr("href") + "/@@wildcard_video_macro",
        success: function (data) {
          var $video = $(data);
          if (width && height) {
            $video.find("[width]").attr("width", width);
            $video.find("[height]").attr("height", height);
          }
          $span.replaceWith($video);
          $video.find("video").mediaelementplayer({
            pluginPath:
              "++resource++wildcard-media/components/mediaelement/build/",
            features: [
              "playpause",
              "current",
              "progress",
              "duration",
              "tracks",
              "volume",
              "fullscreen",
              "googleanalytics",
              "universalgoogleanalytics",
            ],
          });
        },
      });
    });
    $("span.wcaudio a").each(function () {
      var $a = $(this);
      var $span = $a.parents("span.wcaudio");
      var $audio = $(
        '<audio controls="controls" preload="none"' +
          'src="' +
          $a.attr("href") +
          "/@@view/++widget++form.widgets.IAudio.audio_file/@@download/file.mp3" +
          '"></audio>'
      );
      $span.replaceWith($audio);
      $audio.mediaelementplayer({
        features: [
          "playpause",
          "current",
          "progress",
          "duration",
          "tracks",
          "volume",
          "fullscreen",
          "googleanalytics",
          "universalgoogleanalytics",
        ],
      });
    });

    var selector =
      ".template-wildcardvideo #form-widgets-IVideo-upload_video_to_youtube-0";
    var checkFields = function () {
      if ($(selector)[0].checked) {
        $("#formfield-form-widgets-IVideo-video_url").hide();
      } else {
        $("#formfield-form-widgets-IVideo-video_url").show();
      }
    };
    if ($(selector).change(checkFields).size() > 0) {
      checkFields();
    }
  });
});
