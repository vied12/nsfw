(function() {
    'use strict';
    angular.module('nsfw', [
        'ngResource',
        'geocoder-service',
        'ngSanitize',
        'ui.router'
    ])
    .config(['$stateProvider', '$locationProvider',
        function($stateProvider, $locationProvider) {
            $locationProvider.html5Mode({enabled:true}).hashPrefix('#');
            $stateProvider
            .state('home', {
                url: '/',
                controllerAs: 'vm',
                templateUrl: '/home/template.html',
                controller: 'HomeCtrl',
                resolve: {
                    alerts: ['$resource', function($resource) {
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
                        var Alerts = $resource('api/alerts/?limit=3&station=' + stations);
                        return Alerts.get().$promise.then(function(data) {
                            return data.results;
                        });
                    }]
                }
            })
            .state('station', {
                url: '/station/:station/',
                controllerAs: 'vm',
                templateUrl: '/station/template.html',
                controller: 'StationCtrl',
                resolve: {
                    station: ['$stateParams', '$resource', function($stateParams, $resource) {
                        var Stations = $resource('api/stations/' + $stateParams.station  + '/');
                        return Stations.get().$promise;
                    }],
                    alerts: ['$resource', 'station', function($resource, station) {
                        var Alerts = $resource('http://localhost:8000/api/alerts/?limit=10&station=' + station.id + '/');
                        return Alerts.get().$promise.then(function(data) {
                            return data.results;
                        });
                    }]
                }
            });
        }
    ]);
})();
