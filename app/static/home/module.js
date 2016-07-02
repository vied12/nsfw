(function() {
    'use strict';

    function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
        function deg2rad(deg) {
            return deg * (Math.PI/180);
        }
        var R = 6371; // Radius of the earth in km
        var dLat = deg2rad(lat2-lat1);  // deg2rad below
        var dLon = deg2rad(lon2-lon1);
        var a =
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon/2) * Math.sin(dLon/2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        var d = R * c; // Distance in km
        return d;
    }


    HomeCtrl.$inject = ['alerts', 'geocoderService', '$resource', '$q'];
    function HomeCtrl(alerts, geocoderService, $resource, $q) {
        var vm = this;
        angular.extend(vm, {
            alerts: alerts,
            suggestion: undefined,
            search: function() {
                vm.suggestion = undefined;
                var userCoord = geocoderService.getLatLong(vm.address).then(function(latlng){
                    return {lat: latlng.lat(), lon: latlng.lng()};
                });
                var stations = $resource('api/stations/').query().$promise;
                $q.all([userCoord, stations]).then(function(resolved) {
                    var userCoord = resolved[0];
                    var stations = resolved[1];
                    var closest;
                    var distanceMin = 99999;
                    stations.forEach(function(s) {
                        var dist = getDistanceFromLatLonInKm(userCoord.lat, userCoord.lon, s.lat, s.lon);
                        if (dist < distanceMin) {
                            closest = s;
                            distanceMin = dist;
                        }
                    });
                    vm.suggestion = closest;
                });
            }
        });
    }
    angular.module('nsfw')
    .controller('HomeCtrl', HomeCtrl);
})();
