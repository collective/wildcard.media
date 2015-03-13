/* global require */

require([
  'jquery',
  'wildcard-patterns-video'
  ], function($){
  'use strict';

  $(document).ready(function(){
    $('span.wcvideo a').each(function(){
      var $a = $(this);
      var $span = $a.parents('span.wcvideo');
      var width, height;
      if($span.hasClass('video-large')){
        width = 720;
        height = 480;
      }else if($span.hasClass('video-small')){
        width = 320;
        height = 240;
      }
      $.ajax({
        url: $a.attr('href') + '/@@wildcard_video_macro',
        success: function(data){
          var $video = $(data);
          if(width && height){
            $video.find('[width]').attr('width', width);
            $video.find('[height]').attr('height', height);
          }
          $span.replaceWith($video);
          $video.find('video').mediaelementplayer({pluginPath: '++resource++wildcard-media/components/mediaelement/build/'});
        }
      });
    });
    $('span.wcaudio a').each(function(){
      var $a = $(this);
      var $span = $a.parents('span.wcaudio');
      var $audio = $('<audio controls="controls" preload="none"' +
        'src="' + $a.attr('href') + '/@@view/++widget++form.widgets.IAudio.audio_file/@@download/file.mp3' + '"></audio>');
      $span.replaceWith($audio);
      $audio.mediaelementplayer();
    });

  });

});