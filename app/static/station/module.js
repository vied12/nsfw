(function() {
    'use strict';
    StationCtrl.$inject = ['alerts', 'station', 'markers'];
    function StationCtrl(alerts, station, markers) {
        var vm = this;
        angular.extend(vm, {
            station: station,
            alerts: alerts,
            markers: markers,
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
