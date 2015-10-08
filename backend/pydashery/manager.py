import pkgutil
import sys
import json
from tornado import websocket, web, ioloop
from tornado.websocket import WebSocketClosedError
from time import time, sleep
from threading import Thread
import pydashery.widget

# Gets rid of some parent module warnings
import widgets


class Timer(object):
    def __init__(self):
        self.time_elapsed = 0
        self.start_time = None

    def __enter__(self):
        self.start_time = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.time_elapsed = time() - self.start_time


def monitor(manager, widget, wait_time):
    timer = Timer()
    while manager.running:
        timer.time_elapsed = 0
        with timer:
            widget.trigger_update()

        sleep_time = max(wait_time - timer.time_elapsed, 0.0000001)
        sleep(sleep_time)


class Manager(object):
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self.widgets = []
        self.updated_widgets = []
        self.threads = []
        self.webmanager = WebManager(self, logger)
        self.running = True

    def start(self):
        self.logger.info("Starting PyDashery")

        self.load_widgets()
        self.create_widgets()

        wait_time = 1.0 / self.settings.UPDATES_PER_SEC
        self.start_widget_monitors(wait_time)

        try:
            self.webmanager.start(wait_time)
        finally:
            self.logger.info("Cleaning up...")
            self.running = False
            self.webmanager.stop()

    def get_updated_widgets(self):
        updated_widgets, self.updated_widgets = self.updated_widgets, []
        return updated_widgets

    def value_changed(self, widget):
        self.updated_widgets.append(widget)

    def find_widget(self, type):
        classes = pydashery.Widget.__subclasses__()
        for cls in classes:
            if cls.TYPE == type:
                return cls

        raise ValueError("Could not find widget {}".format(type))

    def start_widget_monitors(self, wait_time):
        for widget in self.widgets:
            self.logger.debug(
                "Creating thread for widget {}".format(widget.uuid)
            )

            thread = Thread(target=monitor, args=(self, widget, wait_time))
            self.threads.append(thread)
            thread.start()

    def create_widgets(self):
        for item in self.settings.WIDGETS:
            widget_class = self.find_widget(item["type"])
            widget = widget_class(self, item, self.logger)
            self.widgets.append(widget)

    def load_widgets(self):
        self.logger.debug("Loading widgets")

        dirname = "widgets"
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            path = '%s.%s' % (dirname, package_name)
            if path not in sys.modules:

                module = importer.find_module(package_name).load_module(path)

                self.logger.debug(
                    "Found widget module {}".format(module.__name__))
                for key in dir(module):
                    if key[0] == "_":
                        continue

                    item = getattr(module, key)

                    if item == pydashery.widget.Widget:
                        continue

                    try:
                        if issubclass(item, pydashery.widget.Widget):
                            self.logger.debug(
                                "Found widget {}".format(item.TYPE))
                    except TypeError:
                        pass


def _get_data_handler(webmanager):
    """
    Returns the WebSocket handler, giving it access to the web manager
    :param WebManager webmanager:
    :return tornado.web.RequestHandler:
    """

    class WebSocketHandler(websocket.WebSocketHandler):
        """
        Handler for all communications over WebSockets
        """

        def check_origin(self, origin):
            """
            This is a security protection against cross site scripting attacks
            on browsers, since WebSockets are allowed to bypass the usual
            same-origin policies and don't use CORS headers.
            In the current system there is no need for this yet, thus we allow
            all.
            :param origin:
            :return:
            """

            return True

        def open(self):
            """
            Called when a new connection is opened by a client
            """
            webmanager.on_open(self)

        def on_close(self):
            """
            Called when a client connection is closed
            """
            webmanager.on_close(self)

    return WebSocketHandler


def _get_widget_handler(webmanager):
    """
    Returns a handler to get the widgets
    :param WebManager webmanager:
    :return tornado.web.RequestHandler:
    """

    class WidgetHandler(web.RequestHandler):
        """
        Handler for all communications over WebSockets
        """

        def get(self):
            """
            Called when a client connection is closed
            """
            webmanager.on_get_widgets(self)

    return WidgetHandler


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("../../frontend/index.html")


class WebManager(object):
    def __init__(self, manager, logger):
        self.manager = manager
        self.settings = manager.settings
        self.logger = logger
        self.handlers = []
        self.app = None
        self.loop = None
        self.periodic_callback = None

    def start(self, wait_time):

        handlers = [
            (r'/data', _get_data_handler(self)),
            (r'/widgets', _get_widget_handler(self)),
            (r'/(.+)', web.StaticFileHandler, {"path": "../frontend/"}),
            (r'/', IndexHandler)
        ]

        self.app = web.Application(
            handlers,
            autoreload=self.settings.DEBUG,
            debug=self.settings.DEBUG,
            static_path="../../frontend/"
        )

        self.logger.debug("Listening to {}:{}".format(
            self.settings.LISTEN_PORT,
            self.settings.LISTEN_ADDRESS
        ))

        self.app.listen(
            port=self.settings.LISTEN_PORT,
            address=self.settings.LISTEN_ADDRESS
        )

        def run():
            self.tick()

        self.loop = ioloop.IOLoop.instance()
        self.periodic_callback = ioloop.PeriodicCallback(run, wait_time / 2)
        self.logger.debug("Starting periodic callback")
        self.periodic_callback.start()
        self.logger.debug("Starting IOLoop")
        self.loop.start()

    def stop(self):
        self.periodic_callback.stop()
        self.loop.close()

    def tick(self):
        widgets = self.manager.get_updated_widgets()

        if not widgets:
            return

        data = {}
        for widget in widgets:
            data[widget.uuid] = widget.get_value()

        update = json.dumps(data)
        for handler in self.handlers:
            try:
                handler.write_message(update)
            except WebSocketClosedError:
                self.logger.error("Error writing to client.")

    def on_open(self, handler):
        self.logger.debug("New data stream client from {}".format(
            handler.request.remote_ip
        ))
        self.handlers.append(handler)

    def on_close(self, handler):
        self.logger.debug(
            "Client from {} disconnected from data stream".format(
                handler.request.remote_ip
            ))
        self.handlers.remove(handler)

    def on_get_widgets(self, handler):
        self.logger.debug("Client from {} requested widget list".format(
            handler.request.remote_ip
        ))

        data = []
        for widget in self.manager.widgets:
            data.append(widget.get_widget_info())

        handler.write(json.dumps(data))
