$(function () {
    $.lijie = {
        value_map: new Array(),
        host: '127.0.0.1:8000',
        handle: null,
        sid: null,
        init: function(sid) {
            this.sid = sid;
        },
        get_sid: function() {
            return this.sid;
        },
        bind: function (key, callback) {
            if ( this.value_map[key] === undefined ) {
                this.value_map[key] = new Array();
            }
            this.value_map[key].push(callback);
        },
        query: function () {
            url = ['http://', $.lijie.host, '/monitor/', $.lijie.sid.toString(), '/json/'].join('');
            $.getJSON(url, '', $.lijie.query_success).fail($.lijie.query_fail);
        },
        query_success: function (data, status, xhr) {
            if ( data.href !== undefined ) {
                window.location = data.href;
            }

            for ( key in data.data) {
                var callback_list = $.lijie.value_map[key];
                if ( callback_list === undefined ) {
                    continue
                }
                for ( idx in callback_list) {
                    callback_list[idx](data.data[key]);
                }
            }

            var color = '#303030';
            $("#id_live").animate({color: 'red'}, 'fast');
            $("#id_live").html(data.live + '(' + data.counter + ')');
            $("#id_live").animate({color: color}, 'slow');
        },
        query_fail: function () {
            window.location = '/';
        },
        begin_query: function () {
            this.query();
            this.handle = setInterval(this.query, 1500);
        },
        pause_query: function () {
            clearInterval(this.handle);
        }
    };
});
