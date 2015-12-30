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
        }
    }
})()
