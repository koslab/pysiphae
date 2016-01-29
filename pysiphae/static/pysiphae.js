var pysiphae = new (function () {
    var lock_screen = $('<div id="lock-screen"></div>');
    var spinner = $('<div id="spinner"></div>');
    var has_spinner = false;
    return {
        startSpinner: function () {
            if (!has_spinner) {
                $('body').prepend(lock_screen);
                $('body').prepend(spinner);
                has_spinner = true;
            }
        },
        stopSpinner: function () {
            $('#lock-screen').remove();
            $('#spinner').remove();
            has_spinner = false;
        },
        mapProjection: function(feature, height, width) {
            // create a first guess for the projection
            var center = d3.geo.centroid(feature)
                var scale  = 150;
            var offset = [width/2, height/2];
            var projection = d3.geo.mercator().scale(scale).center(center)
                .translate(offset);

            // create the path
            var path = d3.geo.path().projection(projection);

            // using the path determine the bounds of the current map and use 
            // these to determine better values for the scale and translation
            var bounds  = path.bounds(feature);
            var hscale  = scale*width  / (bounds[1][0] - bounds[0][0]);
            var vscale  = scale*height / (bounds[1][1] - bounds[0][1]);
            var scale   = (hscale < vscale) ? hscale : vscale;
            var offset  = [width - (bounds[0][0] + bounds[1][0])/2,
            height - (bounds[0][1] + bounds[1][1])/2];
            return d3.geo.mercator().center(center)
                .scale(scale).translate(offset);
        }
    }
})()
