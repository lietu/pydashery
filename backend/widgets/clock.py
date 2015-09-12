from datetime import datetime
from pydashery import Widget


class ClockWidget(Widget):
    TYPE = "Clock"
    TEMPLATE = "clock.html"

    def update(self):
        self.set_value(self.get_time())

    def get_time(self):
        if self.settings["24 hours"]:
            format = "%H:%M:%S"
        else:
            format = "%I:%M:%S %p"

        return datetime.now().strftime(format)
