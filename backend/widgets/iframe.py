from pydashery import Widget


class IframeWidget(Widget):
    TYPE = "Iframe"
    TEMPLATE = "iframe.html"

    DEFAULT_SETTINGS = {
        "update_minutes": 0
    }

    def get_update_interval(self):
        return float(self.settings["update_minutes"]) * 60.0

    def update(self):
        self.set_value(self.settings["url"], True)
