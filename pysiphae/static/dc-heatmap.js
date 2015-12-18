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
                return {
                    'x': coord.x,
                    'y': coord.y,
                    'value': _chart.valueAccessor()(d)
                }
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
       
        return _chart.anchor(parent, chartGroup);
    };


    dc.heatmapLeafletChart = function (parent, chartGroup) {
        var _chart = dc.baseMixin({});
        var _width = Infinity;
        var _map;
        var _heatmapLayer;
        var _mapOptions = false;
        var _defaultCenter = false;
        var _defaultZoom = false;
        var _defaultRadius = 10;
        var _defaultMaxOpacity = 0.8;
        var _defaultUseLocalExtrema = false;
        var _defaultScaleRadius = false;

        var _tiles = function (map) {
            L.tileLayer(
                'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
                {
                    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                }
            ).addTo(map);
        };

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

        var _location = function (d) {
            var key = _chart.keyAccessor()(d);
            return {
                'lat': key[0],
                'lng': key[1]
            }
        };


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

            return _chart._doRedraw();
        };

        _chart._doRedraw = function () {
            var groups = _chart._computeOrderedGroups(_chart.data()).filter(function (d) {
                return _chart.valueAccessor()(d) !== 0;
            });

            var data = groups.map(function (d) { 
                var loc = _chart.locationAccessor()(d);
                return {
                    'lat': loc.lat,
                    'lng': loc.lng,
                    'value': _chart.valueAccessor()(d)
                }
            });
            _heatmapLayer.setData({'data': data});
        };

        _chart.locationAccessor = function (_) {
            if (!arguments.length) {
                return _location;
            };

            _location = _;
            return _chart;
        };

        _chart.mapOptions = function (_) {
            if (!arguments.length) {
                return _mapOptions;
            }

            _mapOptions = _;
            return _chart;
        };

        _chart.width = function (_) {
            if (!arguments.length) {
                return _width;
            }

            _width = _;
            return _chart;
        };

        _chart.center = function (_) {
            if (!arguments.length) {
                return _defaultCenter;
            }

            _defaultCenter = _;
            return _chart;
        };

        _chart.zoom = function (_) {
            if (!arguments.length) {
                return _defaultZoom;
            }

            _defaultZoom = _;
            return _chart;
        };

        _chart.radius = function (_) {
            if (!arguments.length) {
                return _defaultRadius;
            }

            _defaultRadius = _;
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

        _chart.tiles = function (_) {
            if (!arguments.length) {
                return _tiles;
            }

            _tiles = _;
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

        _chart.toLocArray = function (value) {
            if (typeof value === 'string') {
                // expects '11.111,1.111'
                value = value.split(',');
            }
            // else expects [11.111,1.111]
            return value;
        };
       
        return _chart.anchor(parent, chartGroup);
    };
})();
