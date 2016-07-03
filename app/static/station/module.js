(function() {
    'use strict';
    StationCtrl.$inject = ['alerts', 'station'];
    function StationCtrl(alerts, station) {
        var vm = this;
        angular.extend(vm, {
            station: station,
            alerts: alerts,
            // markers: markers,
            center: {
                lat: station.lat,
                lng: station.lon,
                zoom: 14
            }
        });
    }
    angular.module('nsfw')
    .controller('StationCtrl', StationCtrl);
})();
