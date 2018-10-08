$(function () {
    $.lijie = {
        value_map: new Array(),
        host: '127.0.0.1:8000',
        handle: null,
        sid: null,
        init: function(sid) {
            this.sid = sid;
        },
        bind: function (key, callback) {
            this.value_map[key] = callback;
        },
        query: function () {
            url = ['http://', $.lijie.host, '/json/monitor/', $.lijie.sid.toString(), '/'].join('');
            $.getJSON(url, '', $.lijie.query_success).fail($.lijie.query_fail);
        },
        query_success: function (data, status, xhr) {
            if ( data.href !== undefined ) {
                window.location = data.href;
            }

            for ( key in data.data) {
                var callback = $.lijie.value_map[key];
                if ( callback === undefined ) {
                    continue
                }
                callback(data.data[key]);
            }
        },
        query_fail: function () {
            window.location = '/';
        },
        begin_query: function () {
            this.query();
            this.handle = setInterval(this.query, 1000);
        },
        pause_query: function () {
            clearInterval(this.handle);
        }
    };
});
