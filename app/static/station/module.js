(function() {
    'use strict';
    StationCtrl.$inject = ['alerts', 'station', 'markers', '$resource'];
    function StationCtrl(alerts, station, markers, $resource) {
        var vm = this;
        angular.extend(vm, {
            subscribe: function() {
                vm.subscribed = false;
                vm.errorOnSubscription = false;
                $resource('/api/subscriptions/').save({
                    email: vm.email,
                    station: station.id
                }).$promise.then(function() {
                    vm.email = '';
                    vm.subscribed = true;
                }, function onError() {
                    vm.errorOnSubscription = true;
                });
            },
            station: station,
            alerts: alerts,
            markers: markers,
            center: {
                lat: station.lat,
                lng: station.lon,
                zoom: 14
            },
            defaults: {
                tileLayer: 'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
                dragging: false,
                scrollWheelZoom: false,
                maxZoom: 18,
            }
        });
    }
    angular.module('nsfw')
    .controller('StationCtrl', StationCtrl);
})();
