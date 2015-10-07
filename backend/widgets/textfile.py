from pydashery import Widget


class TextFileWidget(Widget):
    TYPE = "TextFile"
    TEMPLATE = "textfile.html"

    def update(self):
        self.set_value(self.get_contents())

    def get_contents(self):
        with open(self.settings["filename"], 'r') as f:
            return f.read()
