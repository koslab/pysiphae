(function () {
    'use strict';

    if (dc.heatmapChart) {
        return false;
    }

    dc.heatmapChart = function (parent, chartGroup) {
        var _chart = dc.baseMixin({});

        var _heatmap;

        var _coordinate = function (d) {
            var key = _chart.keyAccessor()(d);
            return {
                'x': key[0],
                'y': key[1]
            }
        };

        var _radiusAccessor = function (d) {
            return null;
        };

        _chart._doRender = function () {
            // render
            //
            d3.select(_chart.anchor())
                .style('height', _chart.height() + 'px')
                .style('width', _chart.width() + 'px');

            _heatmap = h337.create({
                container: _chart.root().node()
            });

            return _chart._doRedraw();
        };

        _chart._doRedraw = function () {
            var groups = _chart._computeOrderedGroups(_chart.data()).filter(function (d) {
                return _chart.valueAccessor()(d) !== 0;
            });
            var data = groups.map(function (d) { 
                var coord = _chart.coordinateAccessor()(d);
                var value = _chart.valueAccessor()(d);
                var result = {
                    'x': coord.x,
                    'y': coord.y,
                    'value': value
                };
                var radius = _chart.radiusAccessor()(d);
                if (radius != null) {
                    result['radius'] = radius;
                };
                return result;
            });
            _heatmap.setData({'data': data});
        };

        _chart.coordinateAccessor = function (_) {
            if (!arguments.length) {
                return _coordinate;
            };

            _coordinate = _;
            return _chart;
        };

        _chart.radiusAccessor = function (_) {
            if (!arguments.length) {
                return _radiusAccessor;
            }

            _radiusAccessor = _;
            return _chart;
        };

        return _chart.anchor(parent, chartGroup);
    };


    dc.heatmapLeafletChart = function (parent, chartGroup) {
        var _chart = dc.leafletMarkerChart(parent, chartGroup);
        var _width = Infinity;
        var _map;
        var _heatmapLayer;
        var _defaultRadius = 10;
        var _defaultMaxOpacity = 0.8;
        var _defaultUseLocalExtrema = false;
        var _defaultScaleRadius = false;
        var _icon = function (d, map) {
            return new L.DivIcon({className: 'hide'});
        };
        var _marker = function (d,map) {
            var marker = new L.Marker(_chart.toLocArray(_chart.locationAccessor()(d)),{
                icon: _icon(),
                clickable: false,
                draggable: false
            });
            return marker;
        };
        var _radiusAccessor = function (d) { return null; };

        _chart.marker(_marker);

        var _heatmap = function (map) {
            _heatmapLayer = new HeatmapOverlay({
                radius: _chart.radius(),
                maxOpacity: _chart.maxOpacity(),
                scaleRadius: _chart.scaleRadius(),
                useLocalExtrema: _chart.useLocalExtrema(),
                latField: 'lat',
                lngField: 'lng',
                valueField: 'value'
            });

            map.addLayer(_heatmapLayer);
        }

        _chart._doRender = function () {
            // render
            //
            _chart.root()
                .style('height', _chart.height() + 'px');

            if (_chart.width() == Infinity) {
                _chart.root().style('width', '100%');
            } else {
                _chart.root().style('width', _chart.width() + 'px');
            }
            var _map = L.map(_chart.root().node(), _chart.mapOptions());

            _chart.heatmap()(_map);

            if (_chart.center() && _chart.zoom()) {
                _map.setView(_chart.toLocArray(_chart.center()), _chart.zoom());
            }

            _chart.tiles()(_map);

            _chart.map(_map);

            _chart._postRender();

            return _chart._doRedraw();
        };

        _chart._markerRedraw = _chart._doRedraw;
        _chart._doRedraw = function () {
            var groups = _chart._computeOrderedGroups(_chart.data()).filter(function (d) {
                return _chart.valueAccessor()(d) !== 0;
            });

            var data = groups.map(function (d) { 
                var loc = _chart.locationAccessor()(d);
                var value = _chart.valueAccessor()(d);
                var result = {
                    'lat': loc[0],
                    'lng': loc[1],
                    'value': value
                };
                var radius = _chart.radiusAccessor()(d);
                if (radius != null) {
                    result['radius'] = radius;
                };
                return result;
            });
            _heatmapLayer.setData({'data': data});
            _chart._markerRedraw();
        };

        _chart.width = function (_) {
            if (!arguments.length) {
                return _width;
            }

            _width = _;
            return _chart;
        };

        _chart.radius = function (_) {
            if (!arguments.length) {
                return _defaultRadius;
            }

            _defaultRadius = _;
            return _chart;
        };

        _chart.radiusAccessor = function (_) {
            if (!arguments.length) {
                return _radiusAccessor;
            }

            _radiusAccessor = _;
            return _chart;
        };

        _chart.maxOpacity = function (_) {
            if (!arguments.length) {
                return _defaultMaxOpacity;
            }

            _defaultMaxOpacity = _;
            return _chart;
        };


        _chart.scaleRadius = function (_) {
            if (!arguments.length) {
                return _defaultScaleRadius;
            }

            _defaultScaleRadius = _;
            return _chart;
        };

        _chart.useLocalExtrema = function (_) {
            if (!arguments.length) {
                return _defaultUseLocalExtrema;
            }

            _defaultUseLocalExtrema = _;
            return _chart;
        };

        _chart.heatmap = function (_) {
            if (!arguments.length) {
                return _heatmap;
            }

            _heatmap = _;
            return _chart;
        };

        _chart.map = function (_) {
            if (!arguments.length) {
                return _map;
            }

            _map = _;
            return _map;
        };

       
        return _chart.anchor(parent, chartGroup);
    };
})();
