
$(document).ready(function () {
    $.lijie.bind('dev', function (dev) {
        $(".id_modbus_dev_model").html(dev.status.dev_model);
    });

    $(".glyphicon-refresh").click(function () {
        $.lijie.query();
    });
    $.lijie.begin_query();
});

