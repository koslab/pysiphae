(function (){
    'use strict';

    if(dc.wordcloudChart){
        return false;
    }

    dc.wordcloudChart = function (parent, chartGroup){
        var _chart = dc.baseMixin({});
        
        var _cloud = null,
            _g = null,
            _svg = null,
            _title = null,
            _text = null,
            _padding = 5,
            _font = "Impact",
            _relativeSize = 10,
            _minX = 0,
            _minY = 0,
            _fill = d3.scale.category20();
        

        _chart._doRender = function (){
            _chart.on('postRender',function(){
                _chart.apply();
            })
            drawWordCloud();

            return _chart;
        }

        function initializeSvg(){

            _chart.select('svg').remove();

            _svg = d3.select(_chart.anchor())
                .append("svg") 
                .attr("height",_chart.height())
                .attr("width",_chart.width())

            _g = _svg
                .append('g')
                //.on('click', _chart.onClick)
                .attr('cursor', 'pointer')
                .attr("width", _chart.width())
                .attr("height", _chart.height())
                .attr("transform", "translate(150,150)")
        }


        function drawWordCloud(){
            initializeSvg();
            
            var groups = _chart._computeOrderedGroups(_chart.data()).filter(function (d){
                return _chart.valueAccessor()(d) !== 0;
            });

            var data = groups.map(function (d){
                var value = _chart.valueAccessor()(d);
                var key = _chart.keyAccessor()(d);
                var title = _chart.title()(d);
                var result = { 
                    'text' : d.key, 
                    'size' : checkSize(d),
                    'value' : value,
                    'key' : key,
                    'title': title
                }

                return result;               
                
            })


            _cloud =  d3.layout.cloud()
                .size([_chart.width(), _chart.height()]);

            _cloud
                .words(data)
                .padding(_chart.padding())
                .font(_chart.font())
                .fontSize(function(d) { 
                    return d.size; 
                })
                .on("end", draw);
            
            _cloud.start();

        }

        function isData() {
            return _isData;
        }
        
        _chart._doRedraw = function (){
            _chart.on('postRedraw',function(){
                _chart.apply();   
            });

           drawWordCloud();
        }

        _chart.apply = function(){
            d3.select(_chart.anchor())
                    .select('svg')
                    .attr("viewBox", _chart.minX()+' '+_chart.minY()+' '+_chart.width()+' '+_chart.height()) 
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
            _text = _g
                    .selectAll("text")
                    .data(words)
                    .enter().append("text")
                    .style("font-size", function(d) { return d.size + "px"; })
                    .style("font-family", _chart.font())
                    .style("fill", function(d, i) { return _fill(i); })
                    .attr("text-anchor", "middle")
                    .attr("class","cloud")
                    .attr("transform", function(d) {
                        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                    })
                    .text(function(d) { return d.text; })
                    .on('click', _chart.onClick)
                    .on('mouseenter', function (d, i) {
                        d3.select(this).attr('stroke', '#303030');
                    })
                    .on('mouseout', function (d, i) {
                        d3.select(this).attr('stroke', 'none');
                    });

            _title = _text
                    .append('title')
                    .text(function(d){return d.title});

            highlightFilter();

        }

        function reDraw(words){

            var groups = _chart._computeOrderedGroups(_chart.data()).filter(function (d){
                return _chart.valueAccessor()(d) !== 0;
            });

            var data = groups.map(function (d){
                var value = _chart.valueAccessor()(d);
                var key = _chart.keyAccessor()(d);
                var title = _chart.title()(d);
                var result = { 
                    'text' : d.key, 
                    'size' : d.font, 
                    'value' : value,
                    'key' : key,
                    'title': title
                }

                return result;               
                
            })

            highlightFilter();
            
        }

        function highlightFilter() {
            if (_chart.hasFilter()) {
                _text.each(function (d) {
                    if (_chart.hasFilter(_chart.keyAccessor()(d))) {
                        _chart.highlightSelected(this);
                    } else {
                        _chart.fadeDeselected(this);
                    }
                });
            } else {
                _text.each(function () {
                    _chart.resetHighlight(this);
                });
            }
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
