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
            controller: function() {
                var vm = this;
                angular.extend(vm, {
                    limits: {
                        PM10: 50,
                        NO2: 200,
                    }
                });
            }
        };
    });
})();
