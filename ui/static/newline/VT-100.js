/**
 * VT-100驱动
 * */


$(document).ready(function () {
    var registers = {
        供液温度: $.modbus.make_hold_register("供液温度", 1, 100, "℃"),
        回液温度: $.modbus.make_hold_register("回液温度", 2, 10, "℃"),
        供液口压力: $.modbus.make_hold_register("供液口压力", 3, 10, "bar"),
        比例阀开度: $.modbus.make_hold_register("比例阀开度", 4, 10, "%"),
        供液口流量: $.modbus.make_hold_register("供液口流量", 5, 100, "L/min")
    };

    create_period_query(1, registers.供液温度);
    create_period_query(1, registers.回液温度);
    create_period_query(1, registers.供液口压力);
    create_period_query(1, registers.比例阀开度);
    create_period_query(1, registers.供液口流量);
});
