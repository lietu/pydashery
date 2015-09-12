(function ($) {
    var PyDashery = function () {
        this.initialize();
    };

    PyDashery.prototype = {
        initialize: function () {
            this.config = {};
            this.widgetClasses = {};
            this.widgets = [];
            this.socket = null;
            this.loadingWidgets = false;

            this.$container = $('.gridster');

            this.gridster = this.$container.gridster({
                widget_margins: [0, 0],
                widget_base_dimensions: [300, 200]
            }).data("gridster");

            this.log("PyDashery initialized");
        },

        start: function () {
            this.log("Starting PyDashery");

            this.connectToDataStream();
        },

        connectToDataStream: function () {
            this.log("Connecting to data source at " + this.config.server.data);

            this.socket = new WebSocket(this.config.server.data);
            this.socket.onopen = this._onSocketConnect.bind(this);
            this.socket.onclose = this._onSocketClose.bind(this);
            this.socket.onmessage = this._onSocketMessage.bind(this);
            this.socket.onerror = this._onSocketError.bind(this);
        },

        loadWidgets: function() {
            if (this.loadingWidgets) {
                return;
            }

            this.loadingWidgets = true;

            this.log("Loading widget info");

            $.get(this.getWidgetURL(), this._onWidgetLoad.bind(this));
        },

        getWidgetURL: function() {
            return (this.config.server.ssl ? 'https://' : 'http://') +
                    this.config.server.host + ':' +
                    this.config.server.port + '/widgets';
        },

        _onWidgetLoad: function(responseText, status, jqxhr) {
            this.log("Widgets loaded");
            this.$container.empty();

            var data = JSON.parse(responseText);
            for (var i = 0, count = data.length; i < count; i++) {
                var info = data[i];

                this.log("Setting up template for " + info.type + " widget " + info.uuid);

                var $template = $(info.template);
                var $item = $template.filter("li");

                $template.remove($item);

                this.$container.append($template);
                this.gridster.add_widget($item[0]);

                this.log("Initializing widget " + info.uuid);
                var widget = new this.widgetClasses[info.type](info.uuid, $template);
                widget.setValue(info.value);

                this.widgets[info.uuid] = widget;
            }

            this.loadingWidgets = false;
        },

        _onSocketConnect: function (event) {
            this.log("Connected to data source");
            this.loadWidgets();
        },

        _onSocketClose: function (event) {
            this.log("Disconnected from data source with code " + event.code);

            this.socket.close();
            this.socket = null;

            this.log("Trying to reconnect.");
            setTimeout(this.connectToDataStream.bind(this), 1000);
        },

        _onSocketMessage: function (event) {
            var data = JSON.parse(event.data);
            var count = 0;
            for (var uuid in data) {
                count++;
                if (!this.widgets[uuid]) {
                    this.log("Whoops, got data for unknown widget " + uuid);
                    this.log("Will try and reload the widgets");
                    this.loadWidgets();
                    return;
                }

                this.widgets[uuid].setValue(data[uuid]);
            }

            if (count) {
                this.log("Processed " + count + " widget update(s)");
            }
        },

        _onSocketError: function (event) {
            this.log("Bumped into some kind of a socket error");
            this.log(event);
        },

        log: function () {
            if (typeof console !== "undefined" && console.log) {
                var args = Array.prototype.slice.apply(arguments);
                console.log.apply(console, args);
            }
        }
    };


    window.pydashery = new PyDashery();
})(window.jQuery);