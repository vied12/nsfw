(function() {
    'use strict';
    StationCtrl.$inject = ['alerts', 'station', 'markers', '$resource'];
    function StationCtrl(alerts, station, markers, $resource) {
        var vm = this;
        var formatDate = d3.time.format('%Y%m%d');
        function getAverage(data) {
            if (!data) {return;}
            var lastYear = new Date();
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            var values = _.map(
                _.filter(data.values, function(v, k) {
                    return parseInt(k) > parseInt(formatDate(lastYear));
                }),
                function(d) {return parseInt(d[0]);}
            );
            if (values.length < 1) {return;}
            var sum = values.reduce(function(a, b) { return a + b; });
            var avg = sum / values.length;
            return avg;
        }
        function getSum(data, limit) {
            if (!data) {return;}
            var lastYear = new Date();
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            var values = _.map(
                _.filter(data.values, function(v, k) {
                    return parseInt(k) > parseInt(formatDate(lastYear)) && v > limit;
                }),
                function(d) {return parseInt(d[0]);}
            );
            return values.length;
        }
        function getLongestStreak(data, limit) {
            if (!data) {return;}
            var lastYear = new Date();
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            var result = [0, null];
            var occurences = 0;
            var reloadCounting = true;
            var dateStart;
            _.forEach(
                _.pick(data.values, function(v, k) {
                    return parseInt(k) > parseInt(formatDate(lastYear));
                }),
                function(v, k) {
                    var value = parseInt(v[0]);
                    if (value >= limit) {
                        if (reloadCounting) {
                            dateStart = k;
                            occurences = 0;
                            reloadCounting = false;
                        }
                        occurences += 1;
                        if (result[0] <= occurences) {
                            var toDate = new Date(formatDate.parse(dateStart));
                            toDate.setDate(toDate.getDate() + occurences);
                            result = [occurences, formatDate.parse(dateStart), toDate];
                        }
                    } else {
                        reloadCounting = true;
                    }
                }
            );
            return result;
        }
        angular.extend(vm, {
            host: location.host,
            subscribe: function() {
                vm.subscribed = false;
                vm.errorOnSubscription = false;
                $resource('/api/subscriptions/').save({
                    email: vm.email,
                    station: station.id
                }).$promise.then(function() {
                    vm.email = '';
                    vm.subscribed = true;
                }, function onError() {
                    vm.errorOnSubscription = true;
                });
            },
            station: station,
            alerts: alerts,
            mp10Average: getAverage(station.pm10_data),
            mp10LongestStreak: getLongestStreak(station.pm10_data, 50),
            mp10Sum: getSum(station.pm10_data, 50),
            // map
            markers: markers,
            center: {
                lat: station.lat,
                lng: station.lon,
                zoom: 12
            },
            defaults: {
                tileLayer: 'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
                dragging: false,
                scrollWheelZoom: false,
                maxZoom: 18,
            }
        });
    }
    angular.module('nsfw')
    .controller('StationCtrl', StationCtrl)
    .directive('nsfwDatavis', function() {
        return {
            scope: {
                station: '='
            },
            link: function(scope, element) {
                var width = 960,
                    height = 156,
                    cellSize = 17; // cell size

                var format = d3.time.format('%Y%m%d'),
                    formatDate = d3.time.format('%d-%m-%Y'),
                    formatMonth = d3.time.format('%B');

                var threshold = d3.scale.threshold()
                    .domain([0, 35, 50])
                    .range(['#fff68d', '#fff68f', 'rgb(227, 161, 140)', '#d9534f']);

                var svg = d3.select(element.get(0)).selectAll('svg')
                    .data(d3.range(2015, 2017).reverse())
                    .enter().append('svg')
                        .attr('width', width)
                        .attr('height', height)
                        .attr('class', 'year')
                        .append('g')
                            .attr('transform', 'translate(' + ((width - cellSize * 53) / 2) + ',' + (height - cellSize * 7 - 1) + ')');

                svg.append('text')
                    .attr('transform', 'translate(-6,' + cellSize * 3.5 + ')rotate(-90)')
                    .style('text-anchor', 'middle')
                    .text(function(d) { return d; });

                var rect = svg.selectAll('.day')
                    .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
                  .enter().append('rect')
                    .attr('class', 'day')
                    .attr('width', cellSize)
                    .attr('height', cellSize)
                    .attr('x', function(d) { return d3.time.weekOfYear(d) * cellSize; })
                    .attr('y', function(d) { return d.getDay() * cellSize; })
                    .datum(format);

                var months = svg.selectAll('.month')
                    .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
                    .enter();
                months.append('text')
                    .attr('style', 'transform: translateY(-5px);')
                    .attr('class', 'month-label')
                    .attr('x', function(d) {
                        var padding = d.getDay() === 0 ? 0 : 1;
                        return (d3.time.weekOfYear(d) + padding) * cellSize;
                    })
                    .text(function(d) { return formatMonth(d); });
                months.append('path')
                    .attr('class', 'month')
                    .attr('d', monthPath);

                    var data = scope.station.pm10_data.values;
                    rect.filter(function(d) { return d in data; })
                    .style('fill', function(d) { return threshold(data[d][0]); })
                    .append('title')
                    .text(function(d) {
                        return formatDate(format.parse(d)) + ': ' + data[d][0] + 'µg/m³';
                    });

                function monthPath(t0) {
                    var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
                        d0 = t0.getDay(), w0 = d3.time.weekOfYear(t0),
                        d1 = t1.getDay(), w1 = d3.time.weekOfYear(t1);
                    return 'M' + (w0 + 1) * cellSize + ',' + d0 * cellSize +
                           'H' + w0 * cellSize + 'V' + 7 * cellSize +
                           'H' + w1 * cellSize + 'V' + (d1 + 1) * cellSize +
                           'H' + (w1 + 1) * cellSize + 'V' + 0 +
                           'H' + (w0 + 1) * cellSize + 'Z';
                }


                // A position encoding for the key only.
                var x = d3.scale.linear()
                    .domain([0, 70])
                    .range([0, 270]);
                var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient('bottom')
                    .tickSize(13)
                    .tickValues(threshold.domain());

                var legend = d3.select(element.get(0)).append('svg')
                    .attr('width', width)
                    .attr('height', height);

                var g = legend.append('g')
                    .attr('class', 'key')
                    .attr('transform', 'translate(' + (width - 240) + ',' + height / 2 + ')');

                g.selectAll('rect')
                    .data(threshold.range().map(function(color) {
                      var d = threshold.invertExtent(color);
                      if (d[0] === undefined) d[0] = x.domain()[0];
                      if (d[1] === undefined) d[1] = x.domain()[1];
                      return d;
                    }))
                  .enter().append('rect')
                    .attr('height', 8)
                    .attr('x', function(d) {return x(d[0]); })
                    .attr('width', function(d) {return x(d[1]) - x(d[0]); })
                    .style('fill', function(d) { return threshold(d[0]); });

                g.call(xAxis)
                .append('text')
                    .attr('class', 'caption')
                    .attr('y', -6)
                    .text('Concentration of PM10 pollution in µg/m³');

            }
        };
    });
})();
