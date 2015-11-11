/* global module */

module.exports = function(grunt) {
  'use strict';

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: {
      all:['build/']
    },
    requirejs: {
      compile: {
        options: {
          baseUrl: './',
          name: 'js/bundle.js',
          mainConfigFile: 'config.js',
          out: 'build/bundle.js',
          stubModules: ['jquery'],
          optimize: 'none',
          paths: {
            'pat-compat': 'empty:',
            'pat-jquery-ext': 'empty:',
            'pat-logger': 'empty:',
            'pat-parser': 'empty:',
            'pat-registry': 'empty:',
            'pat-utils': 'empty:',
            'logging': 'empty:',
            'mockup-parser': 'empty:',
            'mockup-patterns-base': 'empty:',
            'jquery': 'empty:',

            'wildcard-patterns-video': 'js/media-pattern',
            'mediaelement': 'components/mediaelement/build/mediaelement-and-player'
          }
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-requirejs');

  grunt.registerTask('prod', [
    'clean:all',
    'requirejs:compile'
  ]);
};
