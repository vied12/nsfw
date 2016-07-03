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


    HomeCtrl.$inject = ['alerts', 'geocoderService', '$resource', '$q', '$scope', '$state'];
    function HomeCtrl(alerts, geocoderService, $resource, $q, $scope, $state) {
        var vm = this;
        angular.extend(vm, {
            alerts: alerts,
            suggestion: undefined,
            geolocationAvailable: 'geolocation' in navigator,
            searchWhereIam: function() {
                navigator.geolocation.getCurrentPosition(function(position) {
                    vm.search({lat: position.coords.latitude, lon: position.coords.longitude});
                });
            },
            search: function(coord) {
                vm.suggestion = undefined;
                if (!coord) {
                    coord = geocoderService.getLatLong(vm.address).then(function(latlng){
                        return {lat: latlng.lat(), lon: latlng.lng()};
                    });
                }
                var stations = $resource('api/stations/').query().$promise;
                $q.all([$q.when(coord), stations]).then(function(resolved) {
                    var userCoord = resolved[0];
                    var stations = resolved[1];
                    var closest;
                    var distanceMin = 99999;
                    var near = [];
                    stations.forEach(function(s) {
                        var dist = getDistanceFromLatLonInKm(userCoord.lat, userCoord.lon, s.lat, s.lon);
                        if (dist < distanceMin) {
                            closest = s;
                            distanceMin = dist;
                        }
                        if (dist < 100) {
                            near.push(s);
                        }
                    });
                    function createMarker(station, focus) {
                        return {
                            lat: station.lat,
                            lng: station.lon,
                            message: '<a ui-sref="home.station({station: \'' + station.id +'\'})">' + station.name + ' ' + station.id + '</a>',
                            focus: focus
                        };
                    }
                    var markers = {closest: createMarker(closest, true)};
                    near.forEach(function(s) {
                        if (s !== closest) {
                            markers[s.id] = createMarker(s);
                        }
                    });
                    vm.suggestion = {
                        station: closest
                    };
                    $state.go('home.station', {station: closest.id, markers: markers});
                });
            },
            defaults: {
                tileLayer: 'http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
                maxZoom: 18,
                path: {
                    weight: 10,
                    color: '#800000',
                    opacity: 1
                }
            }
        });
    }
    angular.module('nsfw')
    .controller('HomeCtrl', HomeCtrl);
})();
