(function() {
    'use strict';
    StationCtrl.$inject = ['alerts', 'station'];
    function StationCtrl(alerts, station) {
        var vm = this;
        console.log('ssss', alerts, station);
        angular.extend(vm, {
            station: station,
            alerts: alerts
        });
    }
    angular.module('nsfw')
    .controller('StationCtrl', StationCtrl);
})();
