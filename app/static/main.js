(function() {
    'use strict';
    angular.module('nsfw', [
        'ngResource',
        'geocoder-service',
        'ui.bootstrap',
        'ngAnimate',
        'ui-leaflet',
        'gettext',
        'ngSanitize',
        'ui.router'
    ])
    .config(['$stateProvider', '$locationProvider', '$resourceProvider', '$httpProvider',
        function($stateProvider, $locationProvider, $resourceProvider, $httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $resourceProvider.defaults.stripTrailingSlashes = false;
            $locationProvider.html5Mode({enabled:true}).hashPrefix('#');
            $stateProvider
            .state('app', {
                abstract: true,
                controller: ['$stateParams', 'gettextCatalog', function($stateParams, gettextCatalog) {
                    // set language
                    var language = angular.isDefined($stateParams.locale) ? $stateParams.locale : 'de';
                    gettextCatalog.setCurrentLanguage(language);
                    moment.locale(language);
                }],
                template: '<ui-view/>',
                url: '/{locale}/'
            })
            .state('app.home', {
                url: '',
                params: {
                    showOlderAlerts: false
                },
                controllerAs: 'vm',
                templateUrl: '/home/template.html',
                controller: 'HomeCtrl',
                resolve: {
                    alerts: ['$stateParams', '$resource', 'moment',
                    function($stateParams, $resource, moment) {
                        var url = 'api/alerts/?country=de&limit=500';
                        if (!$stateParams.showOlderAlerts) {
                            var x = moment();
                            x.subtract(2, 'days');
                            url += '&max_date='+ x.format('Y-MM-DD');
                        }
                        return $resource(url).get().$promise.then(function(data) {
                            data.results.forEach(function(r) {
                                r.station.name = r.station.name.replace('B ', '');
                            });
                            return data.results;
                        });
                    }]
                }
            })
            .state('app.home.station', {
                url: 'station/:station/',
                params: {
                    markers: []
                },
                controllerAs: 'vm',
                templateUrl: '/station/template.html',
                controller: 'StationCtrl',
                resolve: {
                    markers: ['$stateParams', 'station', function($stateParams, station) {
                        if ($stateParams.markers.length < 1) {
                            return {
                                main: {
                                    lat: station.lat,
                                    lng: station.lon,
                                    message: '<a ui-sref="app.home.station({station: \'' + station.id +'\'})">' + station.name + ' ' + station.id + '</a>',
                                    focus: true
                                }
                            };
                        }
                        angular.forEach($stateParams.markers, function(marker, name) {
                            marker.focus = name === station.id;
                        });
                        return $stateParams.markers;
                    }],
                    station: ['$stateParams', '$resource', function($stateParams, $resource) {
                        var Stations = $resource('api/stations/' + $stateParams.station  + '/');
                        return Stations.get().$promise.then(function(s) {
                            s.pm10_data = JSON.parse(s.pm10_data);
                            s.no2_data = JSON.parse(s.no2_data);
                            // clean data
                            if (s.no2_data) {
                                s.no2_data.values = _.pick(s.no2_data.values, function(v, k) {
                                    return v[0] !== '-999';
                                });
                            }
                            s.name = s.name.replace('B ', '');
                            return s;
                        });
                    }],
                    alerts: ['$resource', 'station', function($resource, station) {
                        var Alerts = $resource('/api/alerts/?limit=10&station=' + station.id);
                        return Alerts.get().$promise.then(function(data) {
                            return data.results;
                        });
                    }]
                }
            })
            .state('app.neukolln', {
                url: 'neukolln/',
                controllerAs: 'vm',
                templateUrl: '/neukolln/template.html',
                controller: 'NeukollnCtrl',
                resolve: {
                    stations: ['$resource', '$q', function($resource, $q) {
                        return $q.all(['DEBE063', 'DEBE064', 'DEBE034'].map(function(id) {
                            return $resource('api/stations/' + id  + '/').get().$promise
                        }))
                    }],
                    luftdaten: ['$resource', function($resource) {
                        return $resource('api/luftdaten?device=0&limit=1').get().$promise
                        .then(function(d) {
                            return d.results[0]
                        })
                    }],
                }
            });
        }
    ])
    .constant('moment', window.moment)
    .run(['gettextCatalog', function (gettextCatalog) {
        gettextCatalog.debug = false;
    }]);
})();
