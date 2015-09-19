from datetime import datetime
from pydashery import Widget


class ClockWidget(Widget):
    TYPE = "Clock"
    TEMPLATE = "clock.html"

    def update(self):
        self.set_value(self.get_time())

    def get_time(self):
        if "format" in self.settings:
            format = self.settings["format"]
        else:
            format = "%Y-%m-%d\n%H:%M:%S"

        return datetime.now().strftime(format)
