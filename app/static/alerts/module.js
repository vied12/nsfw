(function() {
    angular.module('nsfw')
    .directive('lastAlert', function() {
        return {
            scope: {
                hideStation: '@',
                alerts: '='
            },
            templateUrl: 'static/alerts/last.html',
            controllerAs: 'vm',
            bindToController: true,
            controller: ['gettextCatalog', 'gettext', function(gettextCatalog, gettext) {
                var vm = this;
                var tooltip = gettext('{{ value }}µg/m³ is the limit for {{ kind }} pollution based on WHO recommendations');
                function tooltipBody(alert) {
                    return gettextCatalog.getString(tooltip, {
                            kind: alert.report.kind,
                            value: vm.limits[alert.report.kind]
                        }
                    );
                }
                angular.extend(vm, {
                    limits: {
                        PM10: 50,
                        NO2: 200,
                    },
                    tooltipBody: tooltipBody
                });
            }]
        };
    });
})();
