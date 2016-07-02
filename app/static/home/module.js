(function() {
    'use strict';
    HomeCtrl.$inject = ['alerts'];
    function HomeCtrl(alerts) {
        var vm = this;
        angular.extend(vm, {
            alerts: alerts
        });
    }
    angular.module('nsfw')
    .controller('HomeCtrl', HomeCtrl);
})();
