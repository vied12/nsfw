module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
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
                    'po/template.pot': ['app/static/**/*.html', 'app/static/**/*.js', '!app/static/bower_components/**']
                }
            },
        },

    });
    grunt.loadNpmTasks('grunt-angular-gettext');
    grunt.registerTask('extract', ['nggettext_extract']);
    grunt.registerTask('compile', ['nggettext_compile']);
};
