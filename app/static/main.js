(function() {
    'use strict';
    angular.module('nsfw', [
        'ngResource',
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
                    alerts: ['$http', function($http) {
                        return [
                            {
                                report: {
                                    kind: 'PM10'
                                },
                                value: 55
                            },
                            {
                                report: {
                                    kind: 'PM10'
                                },
                                value: 40
                            }
                        ];
                    }]
                }
            });
        }
    ]);
})();
