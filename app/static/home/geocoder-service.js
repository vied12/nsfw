(function(angular){
	'use strict';
	angular.module('geocoder-service', [])
	.factory('geocoderService', [
		'$document',
		'$window',
		'$q',
	function(
		$document,
		$window,
		$q
	) {
		var isloading = false,
			finishedLoading = false,
			callbacks = [],
			geocoder;

		$window.__initMaps = function() {
			finishedLoading = true;
			geocoder = new $window.google.maps.Geocoder();
			for (var x = 0; x < callbacks.length; ++x) {
				callbacks[x].resolve();
			}
			delete $window.__initMaps;
		};

		var geocodeAddress = function(address) {
			var callback = function(address, defer) {
				geocoder.geocode({address: address}, function(results, status){
					if (status === $window.google.maps.GeocoderStatus.OK && results.length > 0) {
						defer.resolve(results);
					} else {
						defer.reject();
					}
				});
			};
			var defer = $q.defer();

				if (!finishedLoading) {
					var d = $q.defer();
					callbacks.push(d);
					d.promise.then(function(){
						callback(address, defer);
					});
					loadGeocoder();
				} else {
					callback(address, defer);
				}
			return defer.promise;
		};

		var loadGeocoder = function() {
			if (isloading) {
				return;
			}
			isloading = true;
			var document = $document[0];
			var script = document.createElement('script');
			script.type = 'text/javascript';
			script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyDMI2J-NcQbd4FOFN-L3u6j8XKIHj7yI68&callback=__initMaps';
			document.body.appendChild(script);
		};
		var obj = {};

		obj.getLatLong = function(address) {
			return obj.getLocations(address).then(function(results){
				if (results.length > 0) {
					return results[0].geometry.location;
				}
				return null;
			});
		};
		obj.getLocations = function(address) {
			return geocodeAddress(address);
		};
		return obj;
	}]);
})(angular);
