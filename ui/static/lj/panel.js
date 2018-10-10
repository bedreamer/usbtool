var p1 = null;
var p2 = null;
var f1 = null;

function update_t(selector, data) {
    $(selector).html([data.toString(), '℃'].join(''));
    if ( data < 10 ) {
        data = 10;
    }
    $(selector).css("width", [data.toString(), '%'].join(''));
}

$(document).ready(function () {
    p1 = new JustGage({
        id: "gauge1",
        value: 67,
        min: 0,
        max: 3,
        gaugeWidthScale: 0.6,
        label: "bar",
        title: "出液压力(P1)"
    });
    p2 = new JustGage({
        id: "gauge2",
        value: 99,
        min: 0,
        max: 3,
        gaugeWidthScale: 0.6,
        label: "bar",
        title: "回液压力(P2)"
    });
    f1 = new JustGage({
        id: "gauge3",
        value: 67,
        min: 0,
        max: 3,
        gaugeWidthScale: 0.6,
        label: "L/min",
        title: "出口流量(F1)"
    });

    $.lijie.bind('dev', function (dev) {
        p1.refresh(dev.data.p1);
        p2.refresh(dev.data.p2);
        f1.refresh(dev.data.f1);

        update_t("#id_T1", dev.data.t1);
        update_t("#id_T2", dev.data.t2);
        update_t("#id_T3", dev.data.t3);
    });

    $(".glyphicon-refresh").click(function () {
        $.lijie.query();
    });
    $.lijie.begin_query();
});

