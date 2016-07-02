(function() {
    'use strict';
    angular.module('nsfw', [
        'ngResource',
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
                        ];
                        var Alerts = $resource('http://localhost:8000/api/alerts/?limit=3&station=' + stations.join(','));
                        return Alerts.get().$promise.then(function(data) {
                            return data.results;
                        });
                    }]
                }
            });
        }
    ]);
})();
