import importlib
from pydashery import Widget


def find_function(search_def):
    """
    Dynamically load the function based on the search definition.

    :param str search_def: A string to tell us the function to load, e.g.
                           module:funcname or module.path:class.staticmethod
    :raises ValueError: In case configuration is invalid
    :return function: A function
    """

    try:
        module_name, funcspec = search_def.split(":")
    except ValueError:
        raise ValueError("Function definition \"{}\" is not valid.".format(
            search_def
        ))

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise ValueError(
            "Function definition \"{}\" is not valid. The module specified "
            "was not found.".format(
                search_def
            )
        )

    if "." in funcspec:
        class_name, func_name = funcspec.split(".")

        try:
            source = getattr(module, class_name)
        except AttributeError:
            raise ValueError(
                "Function definition \"{}\" is not valid. The module does not "
                "contain the specified class.".format(
                    search_def
                )
            )
    else:
        source = module
        func_name = funcspec

    try:
        func = getattr(source, func_name)
    except AttributeError:
        raise ValueError(
            "Function definition \"{}\" is not valid. The function specified "
            "could not be found.".format(
                search_def
            )
        )

    return func


class FunctionResultWidget(Widget):
    TYPE = "FunctionResult"
    TEMPLATE = "functionresult.html"

    DEFAULT_SETTINGS = {
        "update_minutes": 1.0
    }

    def get_update_interval(self):
        return float(self.settings["update_minutes"]) * 60.0

    def update(self):
        self.set_value(self.get_result())

    def get_result(self):
        f = find_function(self.settings["func"])

        return f()
