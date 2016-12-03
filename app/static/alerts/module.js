(function() {
    angular.module('nsfw')
    .service('tooltipBody', ['gettextCatalog', 'gettext', function(gettextCatalog, gettext) {
        var tooltip = gettext('{{ value }}µg/m³ is the limit for {{ kind }} pollution based on WHO recommendations');
        var limits = {
            PM10: 50,
            NO2: 200
        };
        return function(kind, opts) {
            return gettextCatalog.getString(tooltip, {
                    kind: kind,
                    value: limits[kind]
                }
            );
        };
    }])
    .directive('lastAlert', function() {
        return {
            scope: {
                hideStation: '@',
                ordered: '@',
                alerts: '='
            },
            templateUrl: 'static/alerts/last.html',
            controllerAs: 'vm',
            bindToController: true,
            controller: ['tooltipBody', 'moment', function(tooltipBody, moment) {
                var vm = this;
                angular.extend(vm, {
                    moment: moment,
                    tooltipBody: tooltipBody
                });
            }]
        };
    });
})();
