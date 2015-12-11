(function (L) {
    function serializeXmlNode(xmlNode) {
        if (typeof window.XMLSerializer != "undefined") {
            return (new window.XMLSerializer()).serializeToString(xmlNode);
        } else if (typeof xmlNode.xml != "undefined") {
            return xmlNode.xml;
        }
        return "";
    };

    function bakeThePie(options) {
        /*data and valueFunc are required*/
        if (!options.data || !options.valueFunc) {
            return '';
        }
        var data = options.data,
            valueFunc = options.valueFunc,
            r = options.outerRadius?options.outerRadius:28, //Default outer radius = 28px
            rInner = options.innerRadius?options.innerRadius:r-15, //Default inner radius = r-10
            strokeWidth = options.strokeWidth?options.strokeWidth:1, //Default stroke is 1
            pathClassFunc = options.pathClassFunc?options.pathClassFunc:function(){return '';}, //Class for each path
            pathTitleFunc = options.pathTitleFunc?options.pathTitleFunc:function(){return '';}, //Title for each path
            pieClass = options.pieClass?options.pieClass:'marker-cluster-pie', //Class for the whole pie
            pieLabel = options.pieLabel?options.pieLabel:d3.sum(data,valueFunc), //Label for the whole pie
            pieLabelClass = options.pieLabelClass?options.pieLabelClass:'marker-cluster-pie-label',//Class for the pie label
            
            origo = (r+strokeWidth), //Center coordinate
            w = origo*2, //width and height of the svg element
            h = w,
            donut = d3.layout.pie(),
            arc = d3.svg.arc().innerRadius(rInner).outerRadius(r);
            
        //Create an svg element
        var svg = document.createElementNS(d3.ns.prefix.svg, 'svg');
        //Create the pie chart
        var vis = d3.select(svg)
            .data([data])
            .attr('class', pieClass)
            .attr('width', w)
            .attr('height', h);

        vis.append('circle')
            .attr('cx', origo)
            .attr('cy', origo)
            .attr('r', r)
            .attr('fill', 'white')
            .attr('class', 'mycircle');
            
        var arcs = vis.selectAll('g.arc')
            .data(donut.value(valueFunc))
            .enter().append('svg:g')
            .attr('class', 'arc')
            .attr('transform', 'translate(' + origo + ',' + origo + ')');
        
        arcs.append('svg:path')
            .attr('class', pathClassFunc)
            .attr('stroke-width', strokeWidth)
            .attr('d', arc)
            .append('svg:title')
              .text(pathTitleFunc);
                    
        vis.append('text')
            .attr('x',origo)
            .attr('y',origo)
            .attr('class', pieLabelClass)
            .attr('text-anchor', 'middle')
            //.attr('dominant-baseline', 'central')
            /*IE doesn't seem to support dominant-baseline, but setting dy to .3em does the trick*/
            .attr('dy','.3em')
            .text(pieLabel);

        //Return the svg-markup rather than the actual element
        return serializeXmlNode(svg);
    };

    L.Icon.PieChart = function (options) {

        var pie = bakeThePie(options);

        var icon = new L.DivIcon({
            html: pie,
            className: 'marker-cluster',
            iconSize: new L.Point(70, 70)
        });

        return icon;
    }

})(L);
