(function() {
    'use strict';
    NeukollnCtrl.$inject = ['leafletData', 'stations', 'luftdaten'];
    function NeukollnCtrl(leafletData, stations, luftdaten) {
        var formatDate = d3.time.format('%Y%m%d');
        function getLastMeasure(data) {
                if (!data || !data.values) {return;}
                var keys = Object.keys(data.values);
                var lastKey = keys[keys.length - 1];
                if (data.values[lastKey]) {
                    return {
                        value: data.values[lastKey][0],
                        date: formatDate.parse(lastKey)
                    };
                }
        }
        var vm = this;
        var paths = {}
        function createCircle(params) {
            var threshold = d3.scale.threshold()
                .domain([0, 35, 50])
                .range(['#fff68d', '#fff68f', 'rgb(227, 161, 140)', '#d9534f']);
            return {
                type: 'circle',
                fillOpacity: .5,
                weight: 3,
                color: threshold(params.pm_10.value),
                radius: 200,
                latlngs: { lat: params.lat, lng: params.lon },
                message: params.name + '<br/>pm10: ' + params.pm_10.value + '<br/>date: ' + params.pm_10.date,
            }
        }
        stations.forEach(function(s) {
            s.pm_10 = getLastMeasure(JSON.parse(s.pm10_data))
            paths[s.id] = createCircle(s)
        })
        // private stations
        var privateFormatDate = d3.time.format('%Y-%m-%dT%H:%M:%SZ');
        paths['edouard'] = createCircle({
            lat: 52.476857,
            lon: 13.449334,
            name: 'Sonnenallee 176',
            pm_10: { value: luftdaten.SDS_P1, date: privateFormatDate.parse(luftdaten.date) },
        })
        angular.extend(vm, {
            paths: paths,
        })
        // center on markers
        var bounds = Object.keys(paths).map(function(key) {
            return L.marker([paths[key].latlngs.lat, paths[key].latlngs.lng])
        })
        var group = new L.featureGroup(bounds);
        leafletData.getMap().then((map) => {
            map.fitBounds(group.getBounds())
        })
    }

    angular.module('nsfw')
    .controller('NeukollnCtrl', NeukollnCtrl)
    .directive('chart', function() {
        return {
            template: '<svg width="960" height="500"></svg>',
            link: function(scope, element) {
                var svg = d3.select(element.find('svg').get(0)),
                    margin = {top: 20, right: 20, bottom: 30, left: 50},
                    width = +svg.attr('width') - margin.left - margin.right,
                    height = +svg.attr('height') - margin.top - margin.bottom,
                    g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
                var parseTime = d3.time.format('%Y-%m-%dT%H:%M:%SZ');

                var x = d3.time.scale()
                    .rangeRound([0, width]);

                var y = d3.scale.linear()
                    .rangeRound([height, 0]);

                var line = d3.svg.line()
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y(d.SDS_P1); });

                d3.json(`api/luftdaten?device=0&limit=${24*7*2}`, function(data) {
                  data = data.results
                  data.forEach(function(d) {
                      d.date = parseTime.parse(d.date);
                  })
                  x.domain(d3.extent(data, function(d) { return d.date; }));
                  y.domain(d3.extent(data, function(d) { return d.SDS_P1; }));

                  g.append('g')
                      .attr('transform', 'translate(0,' + height + ')')
                      .call(d3.svg.axis().scale(x).orient('bottom'))
                    .select('.domain')
                      .remove();

                  g.append('g')
                      .call(d3.svg.axis().scale(y).orient('left'))
                    .append('text')
                      .attr('fill', '#000')
                      .attr('transform', 'rotate(-90)')
                      .attr('y', 6)
                      .attr('dy', '0.71em')
                      .attr('text-anchor', 'end')
                      .text('PM10');

                  g.append('path')
                      .datum(data)
                      .attr('fill', 'none')
                      .attr('stroke', 'steelblue')
                      .attr('stroke-linejoin', 'round')
                      .attr('stroke-linecap', 'round')
                      .attr('stroke-width', 1.5)
                      .attr('d', line);
                });
            }
        }

    });
})();
