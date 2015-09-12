from uuid import uuid4


class Widget(object):
    TYPE = None
    TEMPLATE = None

    def __init__(self, manager, settings, logger):
        self.manager = manager
        self.settings = settings
        self.logger = logger
        self.value = None
        self.uuid = str(uuid4())

    def set_value(self, value):
        if value != self.value:
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

    def update(self):
        raise NotImplementedError("{} does not implement update".format(
            self.__class__.__name__
        ))
