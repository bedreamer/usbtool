$(document).ready(function () {
    $(".glyphicon-refresh").click(function () {
        $.lijie.query();
    });
    $.lijie.begin_query();
});

