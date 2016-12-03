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


    HomeCtrl.$inject = ['alerts', 'geocoderService', '$resource', '$q', '$state', 'leafletData', 'moment'];
    function HomeCtrl(alerts, geocoderService, $resource, $q, $state, leafletData, moment) {
        var vm = this;
        var markers = {};
        var bounds = [];
        alerts.forEach(function(a) {
            markers[a.id] = {
                lat: a.station.lat,
                lng: a.station.lon,
                message: a.station.name + '<br/>' + a.value + 'µg/m³<br/>' + moment(a.report.date).format('LL')
            }
            bounds.push(L.marker([a.station.lat, a.station.lon]))
        });
        var group = new L.featureGroup(bounds);
        // center on markers
        leafletData.getMap().then((map) => {
            map.fitBounds(group.getBounds())
        })
        angular.extend(vm, {
            $state: $state,
            alerts: alerts.slice(0, 5),
            suggestion: undefined,
            geolocationAvailable: 'geolocation' in navigator,
            markers: markers,
            defaults: {
                // tileLayer: 'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
                tileLayer: 'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
                dragging: true,
                scrollWheelZoom: false,
                maxZoom: 19,
            },
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
                            message: '<a ui-sref="app.home.station({station: \'' + station.id +'\'})">' + station.name + ' ' + station.id + '</a>',
                            focus: focus
                        };
                    }
                    var markers = {};
                    markers[closest.id] = createMarker(closest, true);
                    near.forEach(function(s) {
                        if (s !== closest) {
                            markers[s.id] = createMarker(s);
                        }
                    });
                    vm.suggestion = {
                        station: closest
                    };
                    if (!vm.address) {
                        vm.address = closest.name;
                    }
                    $state.go('app.home.station', {station: closest.id, markers: markers});
                });
            }
        });
    }
    angular.module('nsfw')
    .controller('HomeCtrl', HomeCtrl);
})();
