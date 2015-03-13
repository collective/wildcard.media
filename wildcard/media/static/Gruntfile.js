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
            'pat-compat': 'components/patternslib/src/core/compat',
            'pat-jquery-ext': 'components/patternslib/src/core/jquery-ext',
            'pat-logger': 'components/patternslib/src/core/logger',
            'pat-parser': 'components/patternslib/src/core/parser',
            'pat-registry': 'components/patternslib/src/core/registry',
            'pat-utils': 'components/patternslib/src/core/utils',
            'logging': 'components/logging/src/logging',
            'mockup-parser': 'components/mockup-core/js/parser',
            'mockup-patterns-base': 'components/mockup-core/js/pattern',
            'jquery': 'components/jquery/dist/jquery',

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
