(function (dc) {
    function _setResponsive (chart) {
        var svg = $(chart.anchor() + ' svg');
        var width = svg.attr('width');
        var height = svg.attr('height');
        var el = svg.get(0);
        if (el) {
            el.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
            el.setAttribute('preserveAspectRatio', 'xMidYMid meet');
        }
    }
    
    function setResponsive(group) {
        var charts = dc.chartRegistry.list(group);
        for (var i = 0; i < charts.length; ++i) {
            charts[i].on('postRender', _setResponsive);
            charts[i].on('postRedraw', _setResponsive);
        }
    }

    dc.setResponsive = setResponsive;

})(dc);
