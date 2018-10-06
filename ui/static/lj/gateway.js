var lijie = {
    query = function(host, path, callback) {
        $.getJSON(host, '', path, function(status, data, xhr){
        });
    },
    read = function(modbus_address, name, callback) {
    },
    write = function(modbus_address, name, value, callback) {
    }
}