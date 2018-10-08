var p1 = null;
var p2 = null;
var f1 = null;
$(document).ready(function () {
    p1 = new JustGage({
        id: "gauge1",
        value: 67,
        min: 0,
        max: 3,
        label: "bar",
        title: "出液压力(P1)"
    });
    p2 = new JustGage({
        id: "gauge2",
        value: 99,
        min: 0,
        max: 3,
        label: "bar",
        title: "回液压力(P2)"
    });
    f1 = new JustGage({
        id: "gauge3",
        value: 67,
        min: 0,
        max: 3,
        label: "L/min",
        title: "出口流量(F1)"
    });

    $.lijie.bind('p1', function (data) {
        p1.refresh(data);
    });
    $.lijie.bind('p2', function (data) {
        p2.refresh(data);
    });
    $.lijie.bind('f1', function (data) {
        f1.refresh(data);
    });

    $.lijie.bind('t1', function (data) {
        $("#id_T1").html([data.toString(), '℃'].join(''));
        if ( data < 10 ) {
            data = 10;
        }
        $("#id_T1").css("width", [data.toString(), '%'].join(''));
    });
    $.lijie.bind('t2', function (data) {
        $("#id_T2").html([data.toString(), '℃'].join(''));
        if ( data < 10 ) {
            data = 10;
        }
        $("#id_T2").css("width", [data.toString(), '%'].join(''));
    });
    $.lijie.bind('t3', function (data) {
        $("#id_T3").html([data.toString(), '℃'].join(''));
        if ( data < 10 ) {
            data = 10;
        }
        $("#id_T3").css("width", [data.toString(), '%'].join(''));
    });

    $("a .glyphicon-refresh").click(function () {
        $.lijie.query();
    });
    $.lijie.begin_query();
});

