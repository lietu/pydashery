(function () {
    var ssl = (window.location.protocol === "https");
    var port = window.location.port;
    window.pydashery.config = {
        server: {
            host: window.location.hostname,
            port: port,
            ssl: ssl,
            data: (ssl ? 'wss://' : 'ws://') + window.location.hostname + ':' + port + '/data'
        }
    };
})();
