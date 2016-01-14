(function (){
    'use strict';

    if(dc.wordcloudChart){
        return false;
    }

    dc.wordcloudChart = function (parent, chartGroup){
        var _chart = dc.bubbleMixin(dc.capMixin(dc.bubbleChart(parent)));
        
        var _cloud = null;
        var _g = null;
        var _padding = function(d){return null;};
        var _font = function (d){return null;};
        var _relativeSize = function (d){return null;};
        var _fill = d3.scale.category20();
        
        _chart._doRender = function (){
            _chart.resetSvg();

            _g = _chart.svg().append('g');

            drawCloud();

            return _chart;
        }
        
        _chart._doRedraw = function (){
            drawCloud();

            return _chart;
        }

        function drawCloud(){

            _cloud =  d3.layout.cloud()
                .size([_chart.width(), _chart.height()]);

            _cloud
                .words(_chart.data().map(function (d){
                    return { 
                    text : d.key, 
                    size : checkSize(d)
                    }
                }))
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
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return _fill(i); })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
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
