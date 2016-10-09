module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        // i18nextract: {
        //     default_options: {
        //         src: ['app/static/**/*.html'],
        //         defaultLang: 'en',
        //         lang:     ['en', 'de'],
        //         dest:     'locale'
        //     }
        // }
        nggettext_compile: {
            all: {
                options: {
                    module: 'nsfw'
                },
                files: {
                    'app/static/translations.js': ['po/*.po']
                }
            },
        },
        nggettext_extract: {
            pot: {
                files: {
                    'po/template.pot': ['app/static/**/*.html']
                }
            },
        },

    });
    // grunt.loadNpmTasks('grunt-angular-translate');
    grunt.loadNpmTasks('grunt-angular-gettext');
    // Default task(s).
    grunt.registerTask('extract', ['nggettext_extract']);
    grunt.registerTask('compile', ['nggettext_compile']);
};
