/*
  MODBUS API
* */
// 请求队列
var query_quene = new Array();

// 请求组赛队列
var pendding_quene = new Array();

// 周期查询队列
var period_query_quene = new Array();

// 循环锁
var main_lock = false;


$(function () {
    $.modbus = {
        host: '127.0.0.1:8000',

        /*读寄存器*/
        read: function (sid, modbus_server_address, modbus_register_address, success, fail) {
            var store_key = this.query_idx;
            this.query_idx += 1;

            var url = ['http://', this.host, "/monitor/", sid,
                "/modbus/server/", modbus_server_address,
                "/x03/register/" + modbus_register_address + "/"].join('');

            function on_success(data, status, xhr) {
                pendding_quene.pop();
                return success ? success(data, sid, modbus_server_address, modbus_register_address, xhr) : undefined;
            }
            function on_fail(xhr, status, message) {
                pendding_quene.pop();
                return fail ? fail(status, message, sid, modbus_server_address, modbus_register_address) : undefined;
            }

            $.getJSON(url, '', on_success).fail(on_fail);
        },

        /*写寄存器*/
        write: function (sid, modbus_server_address, modbus_register_address, modbus_value, success, fail) {
            var url = ['http://', this.host, "/monitor/", sid,
                "/modbus/server/", modbus_server_address,
                "/x06/register/" + modbus_register_address +
                "/value/" + modbus_value + "/"].join('');

            function on_success(data, status, xhr) {
                pendding_quene.pop();
                return success ? success(data, sid, modbus_server_address, modbus_register_address, xhr) : undefined;
            }
            function on_fail(xhr, status, message) {
                pendding_quene.pop();
                return fail ? fail(status, message, sid, modbus_server_address, modbus_register_address) : undefined;
            }

            $.getJSON(url, '', on_success).fail(on_fail);
        },

        /*生成一个保持寄存器*/
        make_hold_register: function(name, address, resolution, unit) {
            var register = {
                name: name,
                address: address,
                resolution: resolution,
                unit: unit,
                /*
                    把显示值转换为MODBUS值
                    return 16 bits hex
                * */
                complie_modbus_word: function (display_value) {
                    var v = display_value * this.resolution;
                    return v.toString(16);
                },

                /*
                    把MODBUS值转换为显示值
                */
                complie_display_word: function (modbus_value) {
                    var hex = parseInt(modbus_value, 16);
                    if ( hex & 0x8000 ) {
                        hex |= 0xffff0000;
                        hex = -1 * ~(hex - 1);
                        console.log(hex);
                    }

                    if ( this.resolution === 10 ) {
                        return (hex/10.0).toFixed(1);
                    } else if ( this.resolution === 100 ) {
                        return (hex/100.0).toFixed(2)
                    } else {
                        return hex;
                    }
                },

            };
            return register;
        },

        /*生成一个状态寄存器*/
        make_status_register: function make_status_register(name, address, bitmap) {
            var register = {
                name: name,
                address: address,
                bitmap: bitmap,
            };
            return register;
        }

    };
});

function lock() {
    main_lock = true;
}

function unlock() {
    main_lock = false;
}

function create_read_query(modbus_server_address, register, success, fail) {
    var query = {
        mode: 'read',
        server_address: modbus_server_address,
        register: register,
        success: success,
        fail: fail
    };

    return query;
}

function create_write_query(modbus_server_address, register, display_value, success, fail) {
    var query = {
        mode: 'write',
        server_address: modbus_server_address,
        register: register,
        modbus_value: register.complie_modbus_word(Number(display_value)),
        success: success,
        fail: fail
    };

    return query;
}

function process_query(query) {
    if ( query.mode === 'read' ) {
        $.modbus.read($.lijie.get_sid(), query.server_address, query.register.address, query.success, query.fail);
    } else {
        $.modbus.write($.lijie.get_sid(), query.server_address, query.register.address, query.modbus_value, query.success, query.fail);
    }
}

function create_period_query(modbus_server_address, register, success, fail) {
    var query = create_read_query(modbus_server_address, register, success, fail);
    period_query_quene.push(query);
    return query;
}

function create_a_new_query_quene() {
    var list = new Array();

    // 加入周期查询
    for ( var i = 0; i < period_query_quene.length; i ++ ) {
        var query = period_query_quene[i];
        list.push(query)
    }

    return list;
}

// 主循环
function main()
{
    if (main_lock) {
        return unlock();
    } else {
        lock();
    }

    /*
    请求队列长度不为0则不去新发送请求
    * */
    if ( pendding_quene.length !== 0 ) {
        return unlock();
    }

    /**
     * 新提交的请求还未还未处理，则将未处理的请求附加到阻塞队列
     * */
    if ( query_quene.length !== 0 ) {
        return unlock();
    }

    list = create_a_new_query_quene();
    while ( list.length ) {
        query = list.pop();
        pendding_quene.push(query);
        process_query(query);
    }

    return unlock();
}

setInterval(main, 1500);