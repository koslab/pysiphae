(function (){
    'use strict';

    if(dc.wordcloudChart){
        return false;
    }

    dc.wordcloudChart = function (parent, chartGroup){
        var _chart = dc.baseMixin({});
        
        var _cloud = null,
            _g = null,
            _padding = 5,
            _font = "Impact",
            _relativeSize = 10,
            _minX = 0,
            _minY = 0,
            _fill = d3.scale.category20();
        

        _chart._doRender = function (){
            initializeSvg();
            drawCloud();

            return _chart._doRedraw();
        }

        function initializeSvg(){

            _chart.resetSvg();

            _g = _chart.svg()
                .append('g');
        }
        _chart._doRedraw = function (){
            initializeSvg();
            drawCloud();
            return _chart;
        }

        function drawCloud(){

            var groups = _chart._computeOrderedGroups(_chart.data()).filter(function (d){
                return _chart.valueAccessor()(d) !== 0;
            });

            var data = groups.map(function (d){
                var value = _chart.valueAccessor()(d);
                console.log(value);
                var result = { 
                    'text' : d.key, 
                    'size' : checkSize(d),
                    'value' : value
                }

                return result;               
                
            })

            _cloud =  d3.layout.cloud()
                .size([_chart.width(), _chart.height()]);

            _cloud
                .words(data)
                .padding(_chart.padding())
                .rotate(function() { 
                    return ~~(Math.random() * 2) * 90; 
                })
                .font(_chart.font())
                .fontSize(function(d) { 
                    return d.size; 
                })
                .on("end", draw);

               _cloud.start();

                console.log(d3.select(_chart.anchor())[0]);

        }
        
        function checkSize(d){
            var x = 0;
            if(d.value <= 0) { 
                x = 0
            } else { 
                x = Math.log(d.value)*_chart.relativeSize();
            }
            
            return x;
        }

        function draw(words) {
            _g
            .attr("width", _chart.width())
            .attr("height", _chart.height())
            .attr("transform", "translate(150,150)")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", _chart.font())
            .style("fill", function(d, i) { return _fill(i); })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
        }

        _chart.minX = function (_){
            if(!arguments.length){
                return _minX;
            }
            
            _minX = _;
            return _chart;
        }
        
        _chart.minY = function (_){
            if(!arguments.length){
                return _minY;
            }
            
            _minY = _;
            return _chart;
        }

        _chart.padding = function (_){
            if(!arguments.length){
                return _padding;
            }
            
            _padding = _;
            return _chart;
        }
        
        _chart.font = function (_){
            if(!arguments.length){
                return _font;
            }
            
            _font = _;
            return _chart;
        }
        
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
        
        _chart.relativeSize = function (_){
            if(!arguments.length){
                return _relativeSize;
            }
            
            _relativeSize = _;
            return _chart;
        }

        return _chart.anchor(parent, chartGroup);
    }
})();
