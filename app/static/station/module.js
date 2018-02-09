(function() {
    'use strict';
    var VALUE_KEY = 'Messwert (in µg/m³)'

    StationCtrl.$inject = ['alerts', 'station', 'markers', '$resource', 'moment', 'tooltipBody'];
    function StationCtrl(alerts, station, markers, $resource, moment, tooltipBody) {
        var vm = this;
        var formatDate = d3.time.format('%d.%m.%Y');
        function getLastMeasure(data) {
            if (!data || data.length < 1) {return;}
            return {
                value: data[data.length - 1][VALUE_KEY],
                date: formatDate.parse(data[data.length - 1]['Zeit'])
            }
        }
        function getAverage(data) {
            if (!data) {return;}
            var lastYear = new Date();
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            var values = data.filter(function(v) {
                return formatDate.parse(v['Zeit']) > parseInt(formatDate(lastYear))
            }).map(function(d) {
                return parseInt(d[VALUE_KEY])
            })
            if (values.length < 1) {return;}
            var sum = values.reduce(function(a, b) { return a + b; });
            var avg = sum / values.length;
            return avg;
        }
        function getSum(data, limit) {
            if (!data) {return;}
            var lastYear = new Date();
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            return data
            .filter(function(v) {
                return formatDate.parse(v['Zeit']) > parseInt(formatDate(lastYear))
            })
            .filter(function(d) {
                return parseInt(d[VALUE_KEY]) > limit
            }).length
        }
        function getLongestStreak(data, limit) {
            if (!data) {return;}
            var lastYear = new Date();
            lastYear.setFullYear(lastYear.getFullYear() - 1);
            var result = {value: 0, date: null};
            var occurences = 0;
            var reloadCounting = true;
            var dateStart;
            _.forEach(
                data.filter(function(v) {
                    return formatDate.parse(v['Zeit']) > parseInt(formatDate(lastYear))
                }),
                function(d) {
                    var value = parseInt(d[VALUE_KEY]);
                    if (value >= limit) {
                        if (reloadCounting) {
                            dateStart = d['Zeit'];
                            occurences = 0;
                            reloadCounting = false;
                        }
                        occurences += 1;
                        if (result.value <= occurences) {
                            var toDate = new Date(formatDate.parse(dateStart));
                            toDate.setDate(toDate.getDate() + occurences);
                            result.value = occurences;
                            result.date = formatDate.parse(dateStart);
                            result.toDate = toDate;
                        }
                    } else {
                        reloadCounting = true;
                    }
                }
            );
            return result;
        }
        function dateIsYesterday(date) {
            var yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            return yesterday.toDateString() === date.toDateString();
        }
        angular.extend(vm, {
            moment: moment,
            tooltipBody: tooltipBody,
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
            dateIsYesterday: dateIsYesterday,
            isDatavisPossible: station.pm10_data,
            mp10LastMeasure: getLastMeasure(station.pm10_data),
            mp10Average: getAverage(station.pm10_data),
            mp10LongestStreak: getLongestStreak(station.pm10_data, 50),
            mp10Sum: getSum(station.pm10_data, 50),
            no2LastMeasure: getLastMeasure(station.no2_data),
            no2Average: getAverage(station.no2_data),
            no2LongestStreak: getLongestStreak(station.no2_data, 200),
            no2Sum: getSum(station.no2_data, 200),
            // map
            markers: markers,
            center: {
                lat: station.lat,
                lng: station.lon,
                zoom: 12
            },
            defaults: {
                tileLayer: 'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
                // tileLayer: 'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
                dragging: false,
                scrollWheelZoom: false,
                maxZoom: 19,
            }
        });
    }
    angular.module('nsfw')
    .controller('StationCtrl', StationCtrl)
    .directive('nsfwDatavis', ['$filter', 'gettextCatalog', 'moment', function($filter, gettextCatalog, moment) {
        return {
            scope: {
                station: '='
            },
            link: function(scope, element) {
                var width = 960,
                    height = 156,
                    cellSize = 17; // cell size

                var format = d3.time.format('%d.%m.%Y'),
                    formatDate = d3.time.format('%d-%m-%Y');

                var threshold = d3.scale.threshold()
                    .domain([0, 35, 50])
                    .range(['#fff68d', '#fff68f', 'rgb(227, 161, 140)', '#d9534f']);

                var svg = d3.select(element.get(0)).selectAll('svg')
                    .data(d3.range(2016, new Date().getFullYear() + 1).reverse())
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
                    .text(function(d) { return moment(d).format('MMMM'); });
                months.append('path')
                    .attr('class', 'month')
                    .attr('d', monthPath);

                    var data = scope.station.pm10_data;
                    rect.filter(function(date) {
                        return data.find(function (d) {
                            return d['Zeit'] === date
                        })
                    })
                    .style('fill', function(date) {
                        return threshold(
                            data.find(function (d) {
                                return d['Zeit'] === date
                            })[VALUE_KEY]
                        )
                    })
                    .append('title')
                    .text(function(date) {
                        var value = data.find(function (d) {
                            return d['Zeit'] === date
                        })[VALUE_KEY]
                        return $filter('date')(format.parse(date), 'fullDate') + ': ' +value + 'µg/m³';
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
                    .attr('transform', 'translate(' + 20 + ',' + height / 2 + ')');

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
                    .text(gettextCatalog.getString('Concentration of PM10 particles (µg/m³)'));
            }
        };
    }]);
})();
