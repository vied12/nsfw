(function() {
    'use strict';
    StationCtrl.$inject = ['alerts', 'station'];
    function StationCtrl(alerts, station) {
        var vm = this;
        angular.extend(vm, {
            station: station,
            alerts: alerts
        });
    }
    angular.module('nsfw')
    .controller('StationCtrl', StationCtrl);
})();
