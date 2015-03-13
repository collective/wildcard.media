/* global define */
define([
  'jquery',
  'mockup-patterns-base',
  'mediaelement'
], function($, Base) {
  'use strict';
 
  var Media = Base.extend({
    name: 'media',
    trigger: '.pat-media',
    defaults: {
    },
    init: function() {
      var self = this;
      self.$el.mediaelementplayer({pluginPath: '++resource++wildcard-media/components/mediaelement/build/'});
    }
  });
 
  return Media;
 
});
