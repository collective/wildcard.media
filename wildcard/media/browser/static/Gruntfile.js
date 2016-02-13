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
          out: 'integration.js',
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
            'mediaelement': 'components/mediaelement/build/mediaelement-and-player',
            'mep-feature-googleanalytics': 'components/mediaelement/plugins/mep-feature-googleanalytics',
            'mep-feature-universalgoogleanalytics': 'components/mediaelement/plugins/mep-feature-universalgoogleanalytics'
          }
        }
      },
      compileP4: {
        options: {
          baseUrl: './',
          include: 'js/bundle.js',

          /* use almond + wrap so that this works in Plone 4
             and does not clash with Plone 5 */
          name: 'node_modules/almond/almond.js',
          wrap: true,
          mainConfigFile: 'config.js',
          out: 'integration-p4.js',
          stubModules: ['jquery'],
          optimize: 'none',
          paths: {
            /* sucky thing here is we have to package up all these things..
               Would be nice if there was a plone 4 dependant package
               that would provide these intermediary dependencies that
               would be shared between projects.
               I don't really work on plone 4 though, so I'm not going
               to do anymore work on this */
            'pat-compat': 'components/patternslib/src/core/compat',
            'pat-base': 'components/patternslib/src/core/base',
            'pat-jquery-ext': 'components/patternslib/src/core/jquery-ext',
            'pat-logger': 'components/patternslib/src/core/logger',
            'pat-parser': 'components/patternslib/src/core/parser',
            'pat-registry': 'components/patternslib/src/core/registry',
            'pat-utils': 'components/patternslib/src/core/utils',
            'logging': 'components/logging/src/logging',
            'mockup-parser': 'components/patternslib/src/core/mockup-parser',
            'pat-mockup-parser': 'components/patternslib/src/core/mockup-parser',
            'mockup-patterns-base': 'components/mockup/mockup/patterns/base/pattern',
            'underscore': 'components/underscore/underscore-min',
            'jquery': 'empty:',

            'wildcard-patterns-video': 'js/media-pattern',
            'mediaelement': 'components/mediaelement/build/mediaelement-and-player',
            'mep-feature-googleanalytics': 'components/mediaelement/plugins/mep-feature-googleanalytics',
            'mep-feature-universalgoogleanalytics': 'components/mediaelement/plugins/mep-feature-universalgoogleanalytics'
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
    'requirejs:compile',
    'requirejs:compileP4'
  ]);
};
