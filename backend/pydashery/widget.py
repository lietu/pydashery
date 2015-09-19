from time import time
from uuid import uuid4
from copy import deepcopy


class Widget(object):
    TYPE = None
    TEMPLATE = None

    DEFAULT_SETTINGS = {

    }

    def __init__(self, manager, settings, logger):
        self.manager = manager

        self.settings = deepcopy(self.DEFAULT_SETTINGS)
        self.settings.update(settings)

        self.logger = logger
        self.value = None
        self.uuid = str(uuid4())
        self.update_interval = self.get_update_interval()
        self.next_update = 0

    def get_update_interval(self):
        return 0

    def set_value(self, value, allow_identical=False):
        if value != self.value or allow_identical:
            self.logger.debug("Value for widget {} changed".format(self.uuid))
            self.value = value
            self.manager.value_changed(self)

    def get_value(self):
        return self.value

    def get_widget_info(self):
        return {
            "uuid": self.uuid,
            "type": self.TYPE,
            "value": self.get_value(),
            "template": self.read_template()
        }

    def read_template(self):
        with open("templates/{}".format(self.TEMPLATE)) as f:
            return f.read()

    def trigger_update(self, current_time=None):
        if not current_time:
            current_time = time()

        if self.next_update <= current_time:
            self.next_update = current_time + self.update_interval
            self.update()

    def update(self):
        raise NotImplementedError("{} does not implement update".format(
            self.__class__.__name__
        ))
