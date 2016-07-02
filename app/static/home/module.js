(function() {
    'use strict';
    HomeCtrl.$inject = ['alerts', 'geocoderService'];
    function HomeCtrl(alerts, geocoderService) {
        var vm = this;
        angular.extend(vm, {
            search: function() {
                console.log('s', vm.address);
                geocoderService.getLatLong(vm.address).then(function(latlng){
                    console.log(latlng.lat(), latlng.lng());
                });
            },
            alerts: alerts
        });
    }
    angular.module('nsfw')
    .controller('HomeCtrl', HomeCtrl);
})();
