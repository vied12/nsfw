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
            .state('home', {
                url: '/?ln',
                params: {
                    showOlderAlerts: false
                },
                controllerAs: 'vm',
                templateUrl: '/home/template.html',
                controller: 'HomeCtrl',
                resolve: {
                    alerts: ['$stateParams', '$resource', '$filter', function($stateParams, $resource, $filter) {
                        var stations = [
                            'DEBE069',
                            'DEBE068',
                            'DEBE067',
                            'DEBE066',
                            'DEBE065',
                            'DEBE064',
                            'DEBE063',
                            'DEBE062',
                            'DEBE061',
                            'DEBE056',
                            'DEBE051',
                            'DEBE034',
                            'DEBE032',
                            'DEBE027',
                            'DEBE018',
                            'DEBE010'
                        ].join(',');
                        var url = 'api/alerts/?&limit=3&station=' + stations;
                        if (!$stateParams.showOlderAlerts) {
                            var x = new Date();
                            x.setDate(1);
                            x.setMonth(x.getMonth()-1);
                            var date = $filter('date')(x, 'yyyy-MM-dd');
                            url += '&max_date='+ date;
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
            .state('home.station', {
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
                                    message: '<a ui-sref="home.station({station: \'' + station.id +'\'})">' + station.name + ' ' + station.id + '</a>',
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
                            s.no2_data.values = _.pick(s.no2_data.values, function(v, k) {
                                    return v[0] !== '-999';
                                });
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
            });
        }
    ])
    .constant('moment', window.moment)
    .run(['gettextCatalog', function (gettextCatalog) {
        gettextCatalog.debug = true;
    }]);
})();
